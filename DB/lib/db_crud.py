from .db_client import MongoDBClient
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
import pymongo  # MongoDB 작업을 위한 라이브러리
"""
대형민 주문사항 CREATED_DATA 처럼 상수 파일 따로 만들어서 파일분리해주세요 그리고 DB 사용하는 모든 파일에 import
logging 기능도 넣어주세요
"""
class DbCrud:
    def __init__(self):
        # MongoDB 싱글턴 클라이언트를 통해 데이터베이스와 컬렉션을 가져옴
        self.db = MongoDBClient.get_db()  # 싱글턴 클라이언트를 통해 데이터베이스 가져오기
        self.asset_collection = self.db["test"]  # 데이터베이스에서 컬렉션 가져오기
        
        # **인덱스 생성 (단일 인덱스 추가)**
        self.asset_collection.create_index([("file_format", pymongo.ASCENDING)])
        self.asset_collection.create_index([("updated_at", pymongo.DESCENDING)])
        self.asset_collection.create_index([("downloads", pymongo.DESCENDING)])

    # 데이터 삽입 (Create)
    def insert_one(self, asset_data):
        """
        새로운 자산 데이터를 컬렉션에 삽입합니다.
        :asset_data: 삽입할 자산 데이터 (사전 형태로 전달)
        :return: 삽입된 자산의 ID (문자열 형태)
        """
        # 자산 생성 시간과 수정 시간을 UTC로 추가 (시간대에 상관없는 시간 저장)
        asset_data["created_at"] = datetime.utcnow()  # 생성 시간 추가
        asset_data["updated_at"] = datetime.utcnow()  # 수정 시간 추가
        result = self.asset_collection.insert_one(asset_data)  # asset_data를 MongoDB 컬렉션에 삽입
        return str(result.inserted_id)  # 삽입된 자산의 고유 ID를 반환

    # 데이터 조회 (필터 조건에 맞는 자산 리스트 반환)
    """
    find()는 필터링 된 모든 문서를 가져온 후 limit를 적용하기에 효율성 저하
    aggregate()는 필터링 후 정렬하고, limit를 사용해서 메모리 사용을 줄인다.
    """
    def find(self, filter_conditions=None, sort_by=None, limit=20, skip=0, fields=None):
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
        
        res = list(self.asset_collection.aggregate(pipeline))
        return res

    def find_one(self, asset_id, fields=None):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
        :param asset_id: 자산의 고유 ID
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 자산의 상세 정보 (asset_id, asset_type, description, price 등)
        """
        # 반환할 필드가 있는지 확인하고 프로젝션 준비
        projection = {field: 1 for field in fields} if fields else None

        # 자산 ID로 쿼리 필터 작성
        query_filter = {"_id": ObjectId(asset_id)}  # ObjectId로 변환
        print(f"[DEBUG] Query Filter (ID): {query_filter}")
        print(f"[DEBUG] Projection Fields: {projection}")
        
        # 자산을 찾기 위한 쿼리 실행
        asset_details = self.asset_collection.find_one(query_filter, projection)

        # 자산이 없는 경우 오류 처리
        if not asset_details:
            raise ValueError(f"Asset with ID {asset_id} not found.")
        
        # URL 필드가 없는 경우 기본값 처리
        for url_field in ["particular_url", "turnaround_url", "rig_url"]:
            asset_details[url_field] = asset_details.get(url_field, None)
        
        # 디버깅을 위한 자산 정보 출력
        print(f"[DEBUG] Retrieved Asset Details: {asset_details}")
        
        return asset_details


    # 데이터 수정 (Update)
    def update_one(self, asset_id, update_data):
        """
        기존 자산 데이터를 수정합니다. 만약 자산이 없으면 새로 생성합니다.
        :param asset_id: 수정할 자산의 ID
        :param update_data: 수정할 데이터 (사전 형태)
        :return: 수정 성공 여부 (True/False)
        """
        update_data["updated_at"] = datetime.utcnow()  # 수정 시간을 현재 시간으로 업데이트
        result = self.asset_collection.update_one(
            {"_id": ObjectId(asset_id)},
            {"$set": update_data},
            upsert=True
        )
        return result.acknowledged  # 수정 작업이 성공했으면 True, 실패하면 False 반환

    # 데이터 삭제 (Delete)
    def delete_one(self, asset_id):
        """
        자산을 삭제합니다.
        :param asset_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.asset_collection.delete_one({"_id": ObjectId(asset_id)})  # 자산 ID를 기준으로 삭제
        return result.acknowledged  # 삭제 작업이 성공했으면 True, 실패하면 False 반환

    # 다운로드 수 증가 (Increment Download Count)
    def increment_count(self, asset_id):
        """
        자산의 다운로드 수를 증가시킵니다.
        :param asset_id: 다운로드 수를 증가시킬 자산의 ID
        :return: 다운로드 수 증가 여부 (True/False)
        """
        result = self.asset_collection.update_one(
            {"_id": ObjectId(asset_id)},
            {"$inc": {"downloads": 1}},
        )
        return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환







# 애플리케이션 종료 시 연결 종료
# client.close()


# def get_assets_sorted_by_downloads(limit=10, sort_by_downloads=False):
#     """
#     자산을 다운로드 수(downloads)를 기준으로 정렬하여 조회합니다.
#     :limit: 조회할 데이터 수 (기본값은 10)
#     :sort_by_downloads: 다운로드 순으로 정렬할지 여부
#     :return: 다운로드 수 기준으로 정렬된 자산 리스트
#     """
#     query = asset_collection.find()

#     # 만약 다운로드 수 기준으로 정렬을 원하면 내림차순으로 정렬
#     if sort_by_downloads:
#         query = query.sort("downloads", pymongo.DESCENDING)
#     else:
#         query = query.sort("name", pymongo.ASCENDING)  # 기본적으로 'name' 기준 오름차순 정렬

#     return list(query.limit(limit))  # 조회할 자산 수를 limit으로 제한
