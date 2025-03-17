from db_client import MongoDBClient
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
import pymongo  # MongoDB 작업을 위한 라이브러리

import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../"))+'/utils'
sys.path.append(utils_dir)
from logger import *
from constant import * # 모든 상수 임포트

class DbCrud:
    def __init__(self, logger_name=LOGGER_NAME, log_path = None):
        """
        DbCrud 클래스의 생성자
        - MongoDB 클라이언트를 사용하여 데이터베이스와 컬렉션을 설정합니다.
        - 로깅을 위한 기본 설정을 초기화합니다.

        :param logger_name: 로거 이름 (기본값: LOGGER_NAME)
        :param log_path: 로그 파일 경로 (기본값: None, 제공되지 않으면 기본 로그 경로 사용)
        """
        self.db = MongoDBClient.get_db()  # 싱글턴 클라이언트를 통해 데이터베이스 가져오기
        self.asset_collection = self.db[USER_COLLECTION]  # 데이터베이스에서 컬렉션 가져오기

        default_log_dir = DB_LOGGER_DIR 
        if log_path is None:
            log_path = default_log_dir

        self.logger = create_logger(logger_name, log_path)

    # Create (데이터 생성 또는 업데이트)
    def upsert_data(self, filter_query, data_fields):
        """
        데이터가 없으면 새로 생성하고, 있으면 업데이트하는 범용 메서드.
        :param filter_query: 찾을 조건 (dict)
        :param data_fields: 삽입 또는 업데이트할 필드 (dict)
        :return: 업데이트 또는 삽입된 문서의 ID
        """
        if not data_fields:
            raise ValueError("data_fields는 반드시 제공되어야 합니다.")

        update_data = {
            "$set": {UPDATED_AT: datetime.utcnow()},  # 모든 업데이트에 적용
            "$setOnInsert": {CREATED_AT: datetime.utcnow()}  # 새로 삽입될 경우 적용
        }

        update_data["$set"].update(data_fields)
        update_data["$setOnInsert"].update(data_fields)
        update_data["$setOnInsert"].update(filter_query)  # 필터 조건을 새 데이터에 포함

        # 데이터가 없으면 삽입, 있으면 업데이트
        result = self.asset_collection.update_one(filter_query, update_data, upsert=True)

        if result.upserted_id:
            print(f"새로운 데이터 생성됨: {result.upserted_id}")
        else:
            print(f"기존 데이터 업데이트 완료: {result.modified_count} 개 문서 수정됨")

        return result
    """
    find()는 필터링 된 모든 문서를 가져온 후 limit를 적용하기에 효율성 저하
    aggregate()는 필터링 후 정렬하고, limit를 사용해서 메모리 사용을 줄인다.
    """
    def construct_query_pipeline(self, filter_conditions=None, sort_by=None, sort_order=None,
                                limit=0, skip=0, fields=None,user_quaery =None):
        """
        MongoDB 쿼리 파이프라인을 생성하는 공통 함수.
        :param filter_conditions: 필터 조건 (사전 형태)
        :param sort_by: 정렬 기준 필드
        :param sort_order: 정렬 순서 (ASCENDING or DESCENDING)
        :param limit: 최대 조회 개수
        :param skip: 건너뛸 개수
        :param fields: 반환할 필드 목록
        :param user_quaery: 검색어 기반 검색
        """
        query_filter = {}
        pipeline = []
        projection = {}
        if limit:
            pipeline.append({"$limit": limit})
        if skip:
            pipeline.append({"$skip": skip})

        if filter_conditions:
            for key, value in filter_conditions.items():
                if isinstance(value, list):
                    query_filter[key] = {"$in": value}
                else:
                    query_filter[key] = value
        if user_quaery is not None:
            query_filter["$text"] = {"$search": user_quaery}
            projection["score"]= {"$meta": "textScore"}
            
        if fields:
            for field in fields:
                if field.startswith("$"):  # 필드명이 `$`로 시작하면 오류 발생 가능성 있음
                    raise ValueError(f"[ERROR] Invalid field name: {field}")
                projection[field] = 1
        if projection:
            pipeline.append({"$project": projection})  # 기본 projection            
        pipeline.insert(0,{"$match": query_filter})

        # sort_by만 주어졌을 경우 기본값으로 DESCENDING을 설정
        if user_quaery is not None:
            pipeline.append({"$sort": {"score":-1}})

        elif sort_by:
            default_sort_orders = {
                CREATED_AT: (UPDATED_AT, pymongo.DESCENDING),  # 최신순
                UPDATED_AT: (UPDATED_AT, pymongo.ASCENDING),  # 오래된순
                DOWNLOADS: (DOWNLOADS, pymongo.DESCENDING),    # 다운로드 많은 순
            }
            sort_by, sort_order = default_sort_orders.get(sort_by, (sort_by, pymongo.ASCENDING))  # 기본값 오름차순

        # 정렬 조건 설정
            if user_quaery is None:
                pipeline.append({"$sort": {sort_by: sort_order}})
                print(f"기본 정렬 기준 적용: {sort_by}, {sort_order}")

        self.logger.debug(f"Generated Query Pipeline: {pipeline}")  # 디버깅을 위한 로깅
        print(pipeline)
        return pipeline
    # Read(데이터 조회)
    def find(self, filter_conditions=None, sort_by=None, sort_order=None, limit=0, skip=0, fields=None):
        """
        데이터를 조회하고, 필요한 경우 정렬 및 필터링을 수행합니다.
        :param filter_conditions: 필터 조건 (dict 또는 ObjectId 리스트)
        :param sort_by: 정렬 기준 필드
        :param sort_order: 정렬 순서 (ASCENDING or DESCENDING)
        :param limit: 조회할 데이터 개수
        :param skip: 건너뛸 데이터 개수
        :param fields: 반환할 필드 목록
        :return: 조회된 문서 리스트
        """
        query_filter = {}
        if filter_conditions:
            if isinstance(filter_conditions, list):
                object_ids = []
                for value in filter_conditions:
                    if isinstance(value, str):  # 문자열이면 ObjectId로 변환
                        try:
                            object_ids.append(ObjectId(value))
                        except Exception:
                            raise ValueError(f"Invalid ObjectId format: {value}")
                    elif isinstance(value, ObjectId):  # 이미 ObjectId이면 그대로 사용
                        object_ids.append(value)
                if object_ids:
                    query_filter["_id"] = {"$in": object_ids}
            elif isinstance(filter_conditions, dict):
                query_filter.update(filter_conditions)

        pipeline = self.construct_query_pipeline(query_filter, sort_by, sort_order, limit, skip, fields)

        result = list(self.asset_collection.aggregate(pipeline))
        self.logger.info(f"Query executed with filter: {filter_conditions} | Found: {len(result)} documents")
        
        return result
    
    def find_one(self, object_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
        :param object_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
        """
        projection = {field: 1 for field in fields} if fields else None

        # 자산 ID로 쿼리
        query_filter = {OBJECT_ID: ObjectId(object_id)}  # ObjectId로 변환
        print(f"Query Filter (ID): {query_filter} | Projection Fields: {projection}")
        
        details = self.asset_collection.find_one(query_filter, projection)
        self.logger.info(f"Retrieved document ID: {object_id} | Document Details: {details}")
        return details
    
    def search(self, user_query=None, filter_conditions=None, limit=0, skip=0, fields=None, sort_by=None, sort_order=None):
        """
        검색어 기반으로 데이터를 조회. 검색 점수를 기준으로 정렬됨.
        :param user_query: 사용자 검색어
        :param filter_conditions: 필터 조건 (사전 형태)
        :param limit: 조회할 데이터 개수 제한
        :param skip: 건너뛸 데이터 개수
        :param fields: 반환할 필드 목록
        :param sort_by: 정렬 기준 필드
        :param sort_order: 정렬 순서
        :return: 검색된 문서 리스트
        """
        if fields == None:
            fields = SEARCH_FIELDS

        # 기본 파이프라인 생성
        pipeline = self.construct_query_pipeline(filter_conditions, sort_by, sort_order, limit, skip, fields,user_quaery=user_query)

        # 결과 반환
        result = list(self.asset_collection.aggregate(pipeline))
        
        # 디버깅을 위한 출력
        self.logger.info(f"Search executed with query: {user_query} | Found: {len(result)} documents")
        return result

    # Update(다운로드 수 증가)
    def increment_count(self, object_id, field):
        """
        자산의 다운로드 수를 증가시킵니다.
        :param object_id: 다운로드 수를 증가시킬 자산의 ID
        :return: 다운로드 수 증가 여부 (True/False)
        """
        result = self.asset_collection.update_one(
            {OBJECT_ID: ObjectId(object_id)},
            {"$inc": {field: 1}},
            upsert=False
        )
        self.logger.info(f"Incremented download count for document ID: {object_id}")
        return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환

    # Delete(데이터 삭제)
    def delete_one(self, object_id):
        """
        자산을 삭제합니다.
        :param object_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.asset_collection.delete_one({OBJECT_ID: ObjectId(object_id)})  # 자산 ID를 기준으로 삭제
        self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.acknowledged}")
        return result.acknowledged


# Spirit에서 구현되는 클래스(자식 클래스)
class AssetDb(DbCrud):
    def __init__(self, log_path=None):
        super().__init__(ASSET_LOGGER_NAME, ASSET_LOGGER_DIR)  # 부모 클래스의 생성자 호출
        self.setup_indexes()

    def setup_indexes(self):
            """자산 컬렉션에 대한 인덱스 설정"""
            # self.asset_collection.create_index([(FILE_FORMAT, pymongo.ASCENDING)])
            # self.asset_collection.create_index([(UPDATED_AT, pymongo.DESCENDING)])
            # self.asset_collection.create_index([(UPDATED_AT, pymongo.ASCENDING)])
            # self.asset_collection.create_index([(DOWNLOADS, pymongo.DESCENDING)])
            # self.asset_collection.create_index(
            #     [(NAME, "text")]
            #     # weights={NAME: 10, DESCRIPTION: 1}  # 'name' 필드에 10, 'description' 필드에 1의 가중치 부여
            # )
            # 복합 인덱스 생성 (자식 클래스에서 한 번만 실행)
            # self.asset_collection.create_index(
            #     [("project_name", pymongo.ASCENDING), ("name", pymongo.ASCENDING)], 
            #     unique=True)
            # self.logger.info("Indexes set up for AssetDb")
    # Create (에셋 생성 및 업데이트)
    def upsert_asset(self, project_name, asset_name, data_fields):
        """
        에셋이 없은 경우 새로 생성하고, 있은 경우 업데이트.
        :param project_name: 프로젝트 이름
        :param name: 에셋 이름
        :param update_fields: 업데이트할 필드 (선택 사항)
        """
        if not project_name or not asset_name:
            raise ValueError("필수 필드 'project_name'과 'name'이 제공되지 않았습니다.")
        
        filter_query = {"project_name": project_name, "name": asset_name}
        return self.upsert_data(filter_query, data_fields)