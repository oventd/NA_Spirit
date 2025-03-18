from db_client import MongoDBClient
from bson import ObjectId
from datetime import datetime
import pymongo

import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../"))+'/utils'
sys.path.append(utils_dir)
from logger import *
from constant import * 

class DbCrud:
    def __init__(self, logger_name=LOGGER_NAME, log_path = None):
        """
        DbCrud 클래스의 생성자
        - MongoDB 클라이언트를 사용하여 데이터베이스와 컬렉션을 설정합니다.
        - 로깅을 위한 기본 설정을 초기화합니다.

        :param logger_name: 로거 이름 (기본값: LOGGER_NAME)
        :param log_path: 로그 파일 경로 (기본값: None, 제공되지 않으면 기본 로그 경로 사용)
        """
        self.db = MongoDBClient.get_db()  # 데이터베이스 가져오기
        self.collection = self.db[USER_COLLECTION]  # 데이터베이스에서 컬렉션 가져오기

        default_log_dir = DB_LOGGER_DIR 
        if log_path is None:
            log_path = default_log_dir
        self.logger = create_logger(logger_name, log_path)

    # Create (데이터 생성 또는 업데이트)
    def upsert_data(self, filter_conditions, update_fields):
        """
        데이터가 없으면 새로 생성하고, 있으면 업데이트하는 메서드.
        :param filter_conditions: 찾을 조건 (dict)
        :param update_fields: 삽입 또는 업데이트할 필드 (dict)
        :return: 업데이트 또는 삽입된 문서의 ID
        """
        if not update_fields:
            raise ValueError("data_fields는 기본으로 제공되어야 합니다.")

        update_data = {
            "$set": {UPDATED_AT: datetime.utcnow()},  # 모든 업데이트에 적용
            "$setOnInsert": {CREATED_AT: datetime.utcnow()}  # 새로 삽입될 경우 적용
        }

        update_data["$set"].update(update_fields)
        update_data["$setOnInsert"].update(update_fields)
        update_data["$setOnInsert"].update(filter_conditions)  # 필터 조건을 새 데이터에 포함

        # 데이터가 없으면 삽입, 있으면 업데이트
        result = self.collection.update_one(filter_conditions, update_data, upsert=True)

        if result.upserted_id:
            print(f"새로운 데이터 생성되었습니다.: {result.upserted_id}")
        else:
            print(f"기존 데이터 업데이트 완료: {result.modified_count} 개 문서 수정되었습니다.")
        return result
    
    # Read(조회 쿼리 파이프라인 생성)
    def construct_query_pipeline(self, filter_conditions=None, sort_by=None, sort_order=None,
                                limit=0, skip=0, fields=None, user_query =None):
        """
        MongoDB 쿼리 파이프라인을 생성하는 공통 함수.
        :param filter_conditions: 필터 조건 (사전 형태)
        :param sort_by: 정렬 기준 필드
        :param sort_order: 정렬 순서 (ASCENDING or DESCENDING)
        :param limit: 최대 조회 개수
        :param skip: 건너뛸 개수
        :param fields: 반환할 필드 목록
        :param user_query: 검색어 기반 검색
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

        if user_query is not None:
            query_filter["$text"] = {"$search": user_query}
            projection["score"]= {"$meta": "textScore"}
            
        if fields:
            for field in fields:
                if field.startswith("$"):  # 필드명이 `$`로 시작하면 오류 발생 가능성 있음
                    raise ValueError(f"ERROR Invalid field name: {field}")
                projection[field] = 1
        if projection:
            pipeline.append({"$project": projection})       

        pipeline.insert(0,{"$match": query_filter})

        
        # 검색 기능 sort_by
        sort_conditions = {}
        if user_query is not None:
            sort_conditions["score"] = -1  # 검색 점수 기준 정렬
            default_sort_search = {
                CREATED_AT: (UPDATED_AT, pymongo.DESCENDING),  # 최신순
                UPDATED_AT: (UPDATED_AT, pymongo.ASCENDING),  # 오래된순
                DOWNLOADS: (DOWNLOADS, pymongo.DESCENDING),    # 다운로드 많은 순
            }
            sort_by, sort_order = default_sort_search.get(sort_by, (sort_by, pymongo.ASCENDING))
            if sort_by:  # 정렬 기준이 있을 경우 추가
                sort_conditions[sort_by] = sort_order
            pipeline.append({"$sort": sort_conditions})  # 정렬 적용
            
        # 이외기능의 sort_by
        elif sort_by:
            default_sort_orders = {
                CREATED_AT: (UPDATED_AT, pymongo.DESCENDING),  # 최신순
                UPDATED_AT: (UPDATED_AT, pymongo.ASCENDING),  # 오래된순
                DOWNLOADS: (DOWNLOADS, pymongo.DESCENDING),    # 다운로드 많은 순
            }
            sort_by, sort_order = default_sort_orders.get(sort_by, (sort_by, pymongo.ASCENDING))  # 기본값 오름차순
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
        # query_filter = {}

        # if filter_conditions:
        #     if isinstance(filter_conditions, list):
        #         object_ids = []
        #         for value in filter_conditions:
        #             if isinstance(value, str):  # 문자열이면 ObjectId로 변환합니다.
        #                 try:
        #                     object_ids.append(ObjectId(value))
        #                 except Exception:
        #                     raise ValueError(f"Invalid ObjectId format: {value}")
        #             elif isinstance(value, ObjectId):  # 이미 ObjectId이면 그대로 사용합니다.
        #                 object_ids.append(value)
        #         if object_ids:
        #             query_filter["_id"] = {"$in": object_ids}
        #     elif isinstance(filter_conditions, dict):
        #         query_filter.update(filter_conditions)

        # pipeline = self.construct_query_pipeline(query_filter, sort_by, sort_order, limit, skip, fields)

        # result = list(self.collection.aggregate(pipeline))
        # self.logger.info(f"Query executed with filter: {filter_conditions} | Found: {len(result)} documents")
        
        query_filter = {}

        if isinstance(filter_conditions, list):
            object_ids = []
            for value in filter_conditions:
                if isinstance(value, str):
                    object_ids.append(ObjectId(value))  # 문자열이면 ObjectId로 변환합니다.
                elif isinstance(value, ObjectId):
                    object_ids.append(value)
            query_filter["_id"] = {"$in": object_ids}

        elif isinstance(filter_conditions, dict):
            query_filter.update(filter_conditions)  

        pipeline = self.construct_query_pipeline(query_filter, sort_by, sort_order, limit, skip, fields)

        result = list(self.collection.aggregate(pipeline))
        self.logger.info(f"Query executed with filter: {filter_conditions} | Found: {len(result)} documents")
        return result
    
    def find_one(self, object_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
        :param object_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
        """
        projection = None

        if fields:
            projection = {}
            for field in fields:
                projection[field] = 1

        # 자산 ID로 쿼리
        query_filter = {OBJECT_ID: ObjectId(object_id)}  # ObjectId로 변환
        print(f"Query Filter (ID): {query_filter} | Projection Fields: {projection}")
        
        details = self.collection.find_one(query_filter, projection)
        self.logger.info(f"Retrieved document ID: {object_id} | Document Details: {details}")
        return details
    
    def search(self, filter_conditions=None, limit=0, skip=0, fields=None, sort_by=None, sort_order=None, user_query = None):
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

        pipeline = self.construct_query_pipeline(filter_conditions, sort_by, sort_order, limit, skip, fields, user_query=user_query)

        # 결과 반환
        result = list(self.collection.aggregate(pipeline))
        self.logger.info(f"Search executed with query: {user_query} | Found: {len(result)} documents")
        return result

    # Update(다운로드 수 증가)
    def increment_count(self, object_id, field):
        """
        자산의 다운로드 수를 증가시킵니다.
        :param object_id: 다운로드 수를 증가시킬 자산의 ID
        :return: 다운로드 수 증가 여부 (True/False)
        """
        result = self.collection.update_one(
            {OBJECT_ID: ObjectId(object_id)},
            {"$inc": {field: 1}},
            upsert=False
        )
        self.logger.info(f"Incremented download count for document ID: {object_id}")
        return result.modified_count > 0  

    # Delete(데이터 삭제)
    def delete_one(self, object_id):
        """
        자산을 삭제합니다.
        :param object_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.collection.delete_one({OBJECT_ID: ObjectId(object_id)})  # 자산 ID를 기준으로 삭제
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
    def upsert_asset(self, project_name, asset_name, update_fields):
        """
        에셋이 없은 경우 새로 생성하고, 있은 경우 업데이트.
        :param project_name: 프로젝트 이름
        :param name: 에셋 이름
        :param update_fields: 업데이트할 필드 (선택 사항)
        """
        if not project_name or not asset_name:
            raise ValueError("필수 필드 'project_name'과 'name'이 제공되지 않았습니다~~!")
        
        filter_conditions = {"project_name": project_name, "name": asset_name}
        return self.upsert_data(filter_conditions, update_fields)