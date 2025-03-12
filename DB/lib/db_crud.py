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
"""
대형민 주문사항 CREATED_DATA 처럼 상수 파일 따로 만들어서 파일분리해주세요 그리고 DB 사용하는 모든 파일에 import
logging 기능도 넣어주세요
"""
class DbCrud:
    def __init__(self, logger_name=LOGGER_NAME, log_path = None):
        # MongoDB 싱글턴 클라이언트를 통해 데이터베이스와 컬렉션을 가져옴
        self.db = MongoDBClient.get_db()  # 싱글턴 클라이언트를 통해 데이터베이스 가져오기
        self.asset_collection = self.db[USER_COLLECTION]  # 데이터베이스에서 컬렉션 가져오기

        default_log_dir = DB_LOGGER_DIR 
        if log_path is None:
            log_path = default_log_dir

        self.logger = create_logger(logger_name, log_path)

    # 데이터 삽입 (Create)
    def insert_one(self, asset_data, update_data):
        """
        새로운 자산 데이터를 컬렉션에 삽입합니다.
        :asset_data: 삽입할 자산 데이터 (사전 형태로 전달)
        :return: 삽입된 자산의 ID (문자열 형태)
        """
        # 자산 생성 시간과 수정 시간을 UTC로 추가 (시간대에 상관없는 시간 저장)
        asset_data[CREATED_AT] = datetime.utcnow()  # 생성 시간 추가
        update_data[UPDATED_AT] = datetime.utcnow()  # 수정 시간 추가
        result = self.asset_collection.insert_one(asset_data)  # asset_data를 MongoDB 컬렉션에 삽입
        self.logger.info(f"Inserted document ID: {result.inserted_id} | Asset Data: {asset_data}")
        return str(result.inserted_id)

    """
    find()는 필터링 된 모든 문서를 가져온 후 limit를 적용하기에 효율성 저하
    aggregate()는 필터링 후 정렬하고, limit를 사용해서 메모리 사용을 줄인다.
    """

    def construct_query_pipeline(self, filter_conditions=None, sort_by=None, sort_order=None,
                                limit=40, skip=0, fields=None):
        """
        MongoDB 쿼리 파이프라인을 생성하는 공통 함수.
        - filter_conditions: 필터 조건
        - sort_by: 정렬 기준 필드
        - sort_order: 정렬 순서 (ASCENDING or DESCENDING)
        - limit: 최대 조회 개수
        - skip: 건너뛸 개수
        - fields: 반환할 필드 목록
        """
        query_filter = {}

        if filter_conditions:
            for key, value in filter_conditions.items():
                if isinstance(value, list):
                    query_filter[key] = {"$in": value}
                else:
                    query_filter[key] = value

        projection = None
        if fields:
            projection = {}
            for field in fields:
                projection[field] = 1

        pipeline = [{"$match": query_filter}]

        # sort_by만 주어졌을 경우 기본값으로 DESCENDING을 설정
        if sort_by:
            default_sort_orders = {
                "CREATED_AT": ("CREATED_AT", pymongo.DESCENDING),  # 최신순
                "UPDATED_AT": ("UPDATED_AT", pymongo.ASCENDING),  # 오래된순
                "DOWNLOADS": ("DOWNLOADS", pymongo.DESCENDING),    # 다운로드 많은 순
            }
            sort_by, sort_order = default_sort_orders.get(sort_by, (sort_by, pymongo.ASCENDING))  # 기본값 오름차순

            pipeline.append({"$sort": {sort_by: sort_order}})

        if limit:
            pipeline.append({"$limit": limit})
        if skip:
            pipeline.append({"$skip": skip})
        if projection:
            pipeline.append({"$project": projection})  # 기본 projection

        self.logger.debug(f"Generated Query Pipeline: {pipeline}")  # 디버깅을 위한 로깅
        return pipeline

    def find(self, filter_conditions=None, sort_by=None, sort_order=None, limit=40, skip=0, fields=None):
        pipeline = self.construct_query_pipeline(filter_conditions, sort_by, sort_order, limit, skip, fields)
        result = list(self.asset_collection.aggregate(pipeline))
        self.logger.info(f"Query executed with filter: {filter_conditions} | Found: {len(result)} documents")
        return result

    def find_and_sort(self, filter_conditions=None, sort_by=None, sort_order=None, 
                    limit=40, skip=0, fields=None):
        object_ids = []
        if filter_conditions:
            for value in filter_conditions:
                object_ids.append(ObjectId(value))

        query_filter = {"_id": {"$in": object_ids}}
        pipeline = self.construct_query_pipeline(query_filter, sort_by, sort_order, limit, skip, fields)
        result = list(self.asset_collection.aggregate(pipeline))
        return result
    
    def search(self, user_query=None, filter_conditions=None, limit=40, skip=0, fields=None, sort_by=None, sort_order=None):
        """
        검색어 기반으로 데이터를 조회. 검색 점수를 기준으로 정렬됨.
        """
        pipeline = self.construct_query_pipeline(filter_conditions, sort_by, sort_order, limit, skip, fields)

        if user_query:
            # 텍스트 검색을 위한 파이프라인 추가
            pipeline.append({"$text": {"$search": user_query}})
            pipeline.append({"$sort": {"score": {"$meta": "textScore"}}})  # 점수(score)로 정렬

            # 프로젝션 추가 (필요한 필드 포함)
            projection = {
                "score": {"$meta": "textScore"},
                "_id": 1, "name": 1, "description": 1, "asset_type": 1, "category": 1, 
                "style": 1, "resolution": 1, "file_format": 1, "size": 1, "license_type": 1,
                "creator_id": 1, "creator_name": 1, "downloads": 1, "price": 1, "detail_url": 1,
                "presetting_url1": 1, "presetting_url2": 1, "presetting_url3": 1, "preview_url": 1
            }
        # 만약 fields가 주어지면, 해당 필드들만 포함
        if fields:
            projection = {field: 1 for field in fields}  # fields에 있는 필드들만 1로 설정

            pipeline.append({"$project": projection})

        # 결과 반환
        result = list(self.asset_collection.aggregate(pipeline))
        
        # result에 set_url_fields 적용 (필드값이 None인 경우 기본값 처리)
        result = self.set_url_fields(result)
        
        self.logger.info(f"Search executed with query: {user_query} | Found: {len(result)} documents")
        return result

    def find_one(self, object_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
        :param object_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
        """
        # 반환할 필드가 있는지 확인하고 프로젝션 준비
        projection = {field: 1 for field in fields} if fields else None

        # 자산 ID로 쿼리 필터 작성
        query_filter = {OBJECT_ID: ObjectId(object_id)}  # ObjectId로 변환
        print(f"[DEBUG] Query Filter (ID): {query_filter}")
        print(f"[DEBUG] Projection Fields: {projection}")
        
        # 자산을 찾기 위한 쿼리 실행
        details = self.asset_collection.find_one(query_filter, projection)
        
        # 디버깅을 위한 자산 정보 출력
        print(f"[DEBUG] Retrieved Asset Details: {details}")
        self.logger.info(f"Retrieved document ID: {object_id} | Document Details: {details}")
        return details
    
    # 데이터 수정 (Update)
    def update_one(self, object_id, update_data):
        """
        기존 자산 데이터를 수정합니다. 만약 자산이 없으면 새로 생성합니다.
        :param object_id: 수정할 자산의 ID
        :param update_data: 수정할 데이터 (사전 형태)
        :return: 수정 성공 여부 (True/False)
        """
        update_data[UPDATED_AT] = datetime.utcnow()  # 수정 시간을 현재 시간으로 업데이트
        result = self.asset_collection.update_one(
            {OBJECT_ID: ObjectId(object_id)},
            {"$set": update_data},
            upsert=False
        )
        self.logger.info(f"Updated document ID: {object_id} | Modified: {result.acknowledged}")
        return result.acknowledged

    # 데이터 삭제 (Delete)
    def delete_one(self, object_id):
        """
        자산을 삭제합니다.
        :param object_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.asset_collection.delete_one({OBJECT_ID: ObjectId(object_id)})  # 자산 ID를 기준으로 삭제
        self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.acknowledged}")
        return result.acknowledged

    # 다운로드 수 증가 (Increment Download Count)
    def increment_count(self, object_id, field):
        """
        자산의 다운로드 수를 증가시킵니다.
        :param object_id: 다운로드 수를 증가시킬 자산의 ID
        :return: 다운로드 수 증가 여부 (True/False)
        """
        result = self.asset_collection.update_one(
            {OBJECT_ID: ObjectId(object_id)},
            {"$inc": {field: 1}},
            upsert=True
        )
        self.logger.info(f"Incremented download count for document ID: {object_id}")
        return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환


class AssetDb(DbCrud):
    def __init__(self, log_path=None):
        super().__init__(ASSET_LOGGER_NAME, ASSET_LOGGER_DIR)  # 부모 클래스의 생성자 호출
        self.setup_indexes()

    def setup_indexes(self):
            """자산 컬렉션에 대한 인덱스 설정"""
            # self.asset_collection.create_index([(FILE_FORMAT, pymongo.ASCENDING)])
            # self.asset_collection.create_index([(UPDATED_AT, pymongo.DESCENDING)])
            # self.asset_collection.create_index([(DOWNLOADS, pymongo.DESCENDING)])
            # self.asset_collection.create_index(
            #     [(NAME, TEXT), (DESCRIPTION, TEXT)],
            #     weights={NAME: 10, DESCRIPTION: 1}  # 'name' 필드에 10, 'description' 필드에 1의 가중치 부여
            # )
            self.logger.info("Indexes set up for AssetDb")

    def set_url_fields(self, data):
        """
        자산의 URL 필드를 확인하고, 없는 경우 기본값(None)으로 처리합니다.
        :param data: 자산 데이터 (단일 자산 또는 자산 리스트)
        :return: URL 필드가 설정된 자산 데이터
        """
        url_fields = [DETAIL_URL, PRESETTING_URL1, PRESETTING_URL2,
                    PRESETTING_URL3, TURNAROUND_URL, RIG_URL, APPLY_HDRI, HDRI_URL, MATERIAL_URLS]

        if isinstance(data, list):  # 결과가 리스트인 경우
            for item in data:
                for url_field in url_fields:
                    item[url_field] = item.get(url_field, None)
        else:  # 단일 자산인 경우
            for url_field in url_fields:
                data[url_field] = data.get(url_field, None)
        
        return data
    
    def find(self, filter_conditions=None, sort_by=None, limit=40, skip=0, fields=None):
        """
        자산들을 조회하여 상세 정보를 반환 (필터링, 정렬, 제한, 건너뛰기 등 포함)
        :param filter_conditions: 필터 조건 (기본값은 None)
        :param sort_by: 정렬 기준 (기본값은 None)
        :param limit: 조회할 데이터 수 (기본값은 40)
        :param skip: 건너뛸 데이터 수 (기본값은 0)
        :param fields: 반환할 필드 목록 (기본값은 None)
        :return: 자산들의 상세 정보 리스트
        """
        details = super().find(filter_conditions, sort_by, limit, skip, fields)
        return self.set_url_fields(details)
    
    def find_one(self, object_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환 (AssetDb에서만 사용)
        :param object_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
        """
        # 부모 클래스의 find_one 호출
        details = super().find_one(object_id, fields)
        return self.set_url_fields(details)
    
    def search(self, user_query=None, filter_conditions=None, limit=40, skip=0, fields=None, sort_by=None, sort_order=None):
        # 부모 클래스의 search 호출
        result = super().search(user_query, filter_conditions, limit, skip, fields, sort_by, sort_order)
        return self.set_url_fields(result)

