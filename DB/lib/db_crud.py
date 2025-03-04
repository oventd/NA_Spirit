

# from db_client import MongoDBClient
# from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
# from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
# import pymongo  # MongoDB 작업을 위한 라이브러리
# from db_constant import * # 모든 상수 임포트
# from db_logger import *
# import logging
# import os

# """
# 대형민 주문사항 CREATED_DATA 처럼 상수 파일 따로 만들어서 파일분리해주세요 그리고 DB 사용하는 모든 파일에 import
# logging 기능도 넣어주세요
# """
# class DbCrud:
#     def __init__(self, logger_name=LOGGER_NAME, log_path = None):
#         # MongoDB 싱글턴 클라이언트를 통해 데이터베이스와 컬렉션을 가져옴
#         self.db = MongoDBClient.get_db()  # 싱글턴 클라이언트를 통해 데이터베이스 가져오기
#         self.asset_collection = self.db[USER_COLLECTION]  # 데이터베이스에서 컬렉션 가져오기

#         default_log_dir = DB_LOGGER_DIR 
#         if log_path is None:
#             log_path = default_log_dir

#         self.logger = get_logger(logger_name, log_path)
        

#     # 데이터 삽입 (Create)
#     def insert_one(self, asset_data):
#         """
#         새로운 자산 데이터를 컬렉션에 삽입합니다.
#         :asset_data: 삽입할 자산 데이터 (사전 형태로 전달)
#         :return: 삽입된 자산의 ID (문자열 형태)
#         """
#         # 자산 생성 시간과 수정 시간을 UTC로 추가 (시간대에 상관없는 시간 저장)
#         asset_data[CREATED_AT] = datetime.utcnow()  # 생성 시간 추가
#         asset_data[UPDATED_AT] = datetime.utcnow()  # 수정 시간 추가
#         result = self.asset_collection.insert_one(asset_data)  # asset_data를 MongoDB 컬렉션에 삽입
#         self.logger.info(f"Inserted document ID: {result.inserted_id}")
#         return str(result.inserted_id)  # 삽입된 자산의 고유 ID를 반환

#     # 데이터 조회 (필터 조건에 맞는 자산 리스트 반환)
#     """
#     find()는 필터링 된 모든 문서를 가져온 후 limit를 적용하기에 효율성 저하
#     aggregate()는 필터링 후 정렬하고, limit를 사용해서 메모리 사용을 줄인다.
#     """
#     def find(self, filter_conditions=None, sort_by=None, limit=40, skip=0, fields=None):
#         """
#         필터 조건에 맞는 자산들을 조회합니다.
#         :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
#         :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
#         :param limit: 조회할 데이터 수 (기본값은 20)
#         :param skip: 건너뛸 데이터 수 (기본값은 0)
#         :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
#         :return: 조회된 자산 리스트
#         """
#         if filter_conditions is None:
#             filter_conditions = {}
        
#         query_filter = {}
#         for key, value in filter_conditions.items():
#             if isinstance(value, list):
#                 query_filter[key] = {"$in": value}
#             else:
#                 query_filter[key] = value
        
#         projection = {field: 1 for field in fields} if fields else None
        
#         pipeline = [
#             {"$match": query_filter},  # 🔹 필터링을 먼저 수행하여 데이터 수를 줄임
#             {"$limit": limit},         # 🔹 필요한 개수만 남김
#             {"$skip": skip},           # 🔹 지정된 개수만큼 건너뜀
#             {"$project": projection} if projection else None,  # 🔹 필요한 필드만 선택하여 메모리 사용 절감
#             {"$sort": {sort_by: pymongo.DESCENDING}} if sort_by else None,  # 🔹 정렬 수행 (최대한 데이터를 줄인 후)
#         ]

#         # None 값 제거
#         pipeline = [step for step in pipeline if step]

#             # 🔹 디버깅용 출력
#         print(f"[DEBUG] Query Filter: {query_filter}")
#         print(f"[DEBUG] Projection Fields: {projection}")
#         print(f"[DEBUG] Aggregation Pipeline: {pipeline}")
        
#         result = list(self.asset_collection.aggregate(pipeline))
#         self.logger.info(f"Query executed: {query_filter} | Found: {len(result)}")
#         return result

#     def find_one(self, object_id, fields=None):
#         """
#         자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
#         :param object_id: 자산의 고유 ID
#         :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
#         :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
#         """
#         # 반환할 필드가 있는지 확인하고 프로젝션 준비
#         projection = {field: 1 for field in fields} if fields else None

#         # 자산 ID로 쿼리 필터 작성
#         query_filter = {OBJECT_ID: ObjectId(object_id)}  # ObjectId로 변환
#         print(f"[DEBUG] Query Filter (ID): {query_filter}")
#         print(f"[DEBUG] Projection Fields: {projection}")
        
#         # 자산을 찾기 위한 쿼리 실행
#         details = self.asset_collection.find_one(query_filter, projection)

#         # # 자산이 없는 경우 오류 처리
#         # if not details:
#         #     raise ValueError(f"Asset with ID {object_id} not found.")
        
#         # # URL 필드가 없는 경우 기본값 처리
#         # for url_field in [DETAIL_URL, PRESETTING_URL1, PRESETTING_URL2,
#         #                   PRESETTING_URL3, TURNAROUND_URL, RIG_URL, APPLY_HDRI, HDRI_URL]:
#         #     details[url_field] = details.get(url_field, None)
        
#         # 디버깅을 위한 자산 정보 출력
#         print(f"[DEBUG] Retrieved Asset Details: {details}")
#         self.logger.info(f"Retrieved document ID: {object_id}")
#         return details

#     # 데이터 수정 (Update)
#     def update_one(self, object_id, update_data):
#         """
#         기존 자산 데이터를 수정합니다. 만약 자산이 없으면 새로 생성합니다.
#         :param object_id: 수정할 자산의 ID
#         :param update_data: 수정할 데이터 (사전 형태)
#         :return: 수정 성공 여부 (True/False)
#         """
#         update_data[UPDATED_AT] = datetime.utcnow()  # 수정 시간을 현재 시간으로 업데이트
#         result = self.asset_collection.update_one(
#             {OBJECT_ID: ObjectId(object_id)},
#             {"$set": update_data},
#             upsert=False
#         )
#         self.logger.info(f"Updated document ID: {object_id} | Modified: {result.acknowledged}")
#         return result.acknowledged  # 수정 작업이 성공했으면 True, 실패하면 False 반환

#     # 데이터 삭제 (Delete)
#     def delete_one(self, object_id):
#         """
#         자산을 삭제합니다.
#         :param object_id: 삭제할 자산의 ID
#         :return: 삭제 성공 여부 (True/False)
#         """
#         result = self.asset_collection.delete_one({OBJECT_ID: ObjectId(object_id)})  # 자산 ID를 기준으로 삭제
#         self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.acknowledged}")
#         return result.acknowledged  # 삭제 작업이 성공했으면 True, 실패하면 False 반환

#     # 다운로드 수 증가 (Increment Download Count)
#     def increment_count(self, object_id, field):
#         """
#         자산의 다운로드 수를 증가시킵니다.
#         :param object_id: 다운로드 수를 증가시킬 자산의 ID
#         :return: 다운로드 수 증가 여부 (True/False)
#         """
#         result = self.asset_collection.update_one(
#             {OBJECT_ID: ObjectId(object_id)},
#             {"$inc": {field: 1}},
#         )
#         self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.modified_count}")
#         return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환

#     # 데이터 검색 (Search)
#     def search(self, user_query):
#         """
#         데이터에 대한 검색 기능을 수행합니당.
#         :user_query: 검색을 진행할 데이터
#         :return: 검색 결과
#         """
#         query = { "$text": { "$search": user_query } }
#         projection = { NAME: 1, "_id": 0, SCORE: { "$meta": "textScore" } }  # name 필드와 점수 가져오기
        
#         results = (
#             self.asset_collection.find(query, projection)
#             .sort([(SCORE, {"$meta": "textScore"})])  # 정확도 순 정렬
#             .limit(10)  # 최대 10개 제한
#         )
#         result_list = list(results)
#         return result_list


# class UserDb(DbCrud):
#     def __init__(self, log_path=None):
#         super().__init__(ASSET_LOGGER_NAME, ASSET_LOGGER_DIR)  # 부모 클래스의 생성자 호출
#         self.setup_indexes()

#     def setup_indexes(self):
#         """자산 컬렉션에 대한 인덱스 설정"""
#         self.asset_collection.create_index([(FILE_FORMAT, pymongo.ASCENDING)])
#         self.asset_collection.create_index([(UPDATED_AT, pymongo.DESCENDING)])
#         self.asset_collection.create_index([(DOWNLOADS, pymongo.DESCENDING)])
#         self.asset_collection.create_index([(NAME, TEXT), (DESCRIPTION, TEXT)])
#         self.logger.info("Indexes set up for UserDb")

    

from db_client import MongoDBClient
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
import pymongo  # MongoDB 작업을 위한 라이브러리
from db_constant import * # 모든 상수 임포트
from db_logger import *
import logging
import os

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

        self.logger = get_logger(logger_name, log_path)
        

    # 데이터 삽입 (Create)
    def insert_one(self, asset_data):
        """
        새로운 자산 데이터를 컬렉션에 삽입합니다.
        :asset_data: 삽입할 자산 데이터 (사전 형태로 전달)
        :return: 삽입된 자산의 ID (문자열 형태)
        """
        # 자산 생성 시간과 수정 시간을 UTC로 추가 (시간대에 상관없는 시간 저장)
        asset_data[CREATED_AT] = datetime.utcnow()  # 생성 시간 추가
        asset_data[UPDATED_AT] = datetime.utcnow()  # 수정 시간 추가
        result = self.asset_collection.insert_one(asset_data)  # asset_data를 MongoDB 컬렉션에 삽입
        self.logger.info(f"Inserted document ID: {result.inserted_id}")
        return str(result.inserted_id)  # 삽입된 자산의 고유 ID를 반환

    # 데이터 조회 (필터 조건에 맞는 자산 리스트 반환)
    """
    find()는 필터링 된 모든 문서를 가져온 후 limit를 적용하기에 효율성 저하
    aggregate()는 필터링 후 정렬하고, limit를 사용해서 메모리 사용을 줄인다.
    """
    def find(self, filter_conditions=None, sort_by=None, limit=40, skip=0, fields=None):
        """
        필터 조건에 맞는 자산들을 조회합니다.
        :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
        :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
        :param limit: 조회할 데이터 수 (기본값은 20)
        :param skip: 건너뛸 데이터 수 (기본값은 0)
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 조회된 자산 리스트
        """
        if filter_conditions is None:
            filter_conditions = {}
        
        query_filter = {}
        for key, value in filter_conditions.items():
            if isinstance(value, list):
                query_filter[key] = {"$in": value}
            else:
                query_filter[key] = value
        
        projection = {field: 1 for field in fields} if fields else None
        
        pipeline = [
            {"$match": query_filter},  # 🔹 필터링을 먼저 수행하여 데이터 수를 줄임
            {"$limit": limit},         # 🔹 필요한 개수만 남김
            {"$skip": skip},           # 🔹 지정된 개수만큼 건너뜀
            {"$project": projection} if projection else None,  # 🔹 필요한 필드만 선택하여 메모리 사용 절감
            {"$sort": {sort_by: pymongo.DESCENDING}} if sort_by else None,  # 🔹 정렬 수행 (최대한 데이터를 줄인 후)
        ]

        # None 값 제거
        pipeline = [step for step in pipeline if step]

            # 🔹 디버깅용 출력
        print(f"[DEBUG] Query Filter: {query_filter}")
        print(f"[DEBUG] Projection Fields: {projection}")
        print(f"[DEBUG] Aggregation Pipeline: {pipeline}")
        
        result = list(self.asset_collection.aggregate(pipeline))
        self.logger.info(f"Query executed: {query_filter} | Found: {len(result)}")
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
        self.logger.info(f"Retrieved document ID: {object_id}")
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
        return result.acknowledged  # 수정 작업이 성공했으면 True, 실패하면 False 반환

    # 데이터 삭제 (Delete)
    def delete_one(self, object_id):
        """
        자산을 삭제합니다.
        :param object_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.asset_collection.delete_one({OBJECT_ID: ObjectId(object_id)})  # 자산 ID를 기준으로 삭제
        self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.acknowledged}")
        return result.acknowledged  # 삭제 작업이 성공했으면 True, 실패하면 False 반환

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
        )
        self.logger.info(f"Deleted document ID: {object_id} | Acknowledged: {result.modified_count}")
        return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환

    # 데이터 검색 (Search)
    def search(self, user_query):
        """
        데이터에 대한 검색 기능을 수행합니당.
        :user_query: 검색을 진행할 데이터
        :return: 검색 결과
        """
        query = { "$text": { "$search": user_query } }
        projection = { NAME: 1, "_id": 0, SCORE: { "$meta": "textScore" } }  # name 필드와 점수 가져오기
        
        results = (
            self.asset_collection.find(query, projection)
            .sort([(SCORE, {"$meta": "textScore"})])  # 정확도 순 정렬
            .limit(10)  # 최대 10개 제한
        )
        result_list = list(results)
        return result_list


class UserDb(DbCrud):
    def __init__(self, log_path=None):
        super().__init__(ASSET_LOGGER_NAME, ASSET_LOGGER_DIR)  # 부모 클래스의 생성자 호출
        self.setup_indexes()

    def setup_indexes(self):
        """자산 컬렉션에 대한 인덱스 설정"""
        self.asset_collection.create_index([(FILE_FORMAT, pymongo.ASCENDING)])
        self.asset_collection.create_index([(UPDATED_AT, pymongo.DESCENDING)])
        self.asset_collection.create_index([(DOWNLOADS, pymongo.DESCENDING)])
        self.asset_collection.create_index([(NAME, TEXT), (DESCRIPTION, TEXT)])
        self.logger.info("Indexes set up for UserDb")

    def find_one(self, object_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환 (UserDb에서만 사용)
        :param object_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (object_id, asset_type, description, price 등)
        """
        # 부모 클래스의 find_one 호출
        details = super().find_one(object_id, fields)

        # URL 필드가 없는 경우 기본값 처리
        if details:
            for url_field in [DETAIL_URL, PRESETTING_URL1, PRESETTING_URL2,
                              PRESETTING_URL3, TURNAROUND_URL, RIG_URL, APPLY_HDRI, HDRI_URL, MATERIAL_URLS]:
                details[url_field] = details.get(url_field, None)

        return details
    
    def find(self, filter_conditions=None, sort_by=None, limit=40, skip=0, fields=None):
        details = super().find(filter_conditions, sort_by, limit, skip, fields)
            # URL 필드가 없는 경우 기본값 처리
        if details:
            for url_field in [DETAIL_URL, PRESETTING_URL1, PRESETTING_URL2,
                              PRESETTING_URL3, TURNAROUND_URL, RIG_URL, APPLY_HDRI, HDRI_URL, MATERIAL_URLS]:
                details[url_field] = details.get(url_field, None)

        return details
    
    def search(self, user_query):
        return super().search(user_query)