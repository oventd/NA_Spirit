from .db_client import MongoDBClient
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
import pymongo  # MongoDB 작업을 위한 라이브러리



class Crud:
    def __init__(self):
        # MongoDB 싱글턴 클라이언트를 통해 데이터베이스와 컬렉션을 가져옴
        self.db = MongoDBClient.get_db()  # 싱글턴 클라이언트를 통해 데이터베이스 가져오기
        self.asset_collection = self.db["test"]  # 데이터베이스에서 컬렉션 가져오기
        
        # **인덱스 생성 (단일 인덱스 추가)**
        self.asset_collection.create_index([("file_format", pymongo.ASCENDING)])
        self.asset_collection.create_index([("updated_at", pymongo.DESCENDING)])
        self.asset_collection.create_index([("downloads", pymongo.DESCENDING)])

    # 데이터 삽입 (Create)
    def insert_asset(self, asset_data):
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
    def get_assets(self, filter_conditions=None, sort_by=None, limit=20, skip=0):
        """
        필터 조건에 맞는 자산들을 조회합니다.
        :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
        :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
        :param limit: 조회할 데이터 수 (기본값은 20)
        :param skip: 건너뛸 데이터 수 (기본값은 0)
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

        pipeline = [
            {"$match": query_filter},  # 🔹 필터 적용
            {"$skip": skip},  # 🔹 건너뛰기 (skip 값 적용)
            {"$limit": limit},  # 🔹 필요한 개수만 남기기
            {"$project": {  # 🔹 필요한 필드만 선택
                "name": 1,
                "preview_url": 1,
                "thumbnail_url": 1,
                "asset_type": 1,
                "_id": 1
            }},
            {"$sort": {sort_by: pymongo.DESCENDING}} if sort_by else None  # 🔹 정렬 (필요한 경우)
        ]
        
        # None 값 제거 (sort_by가 없으면 해당 단계 삭제)
        pipeline = [step for step in pipeline if step]

        res = list(self.asset_collection.aggregate(pipeline))
        return res


    # 세부 데이터 조회 (필터 조건에 맞는 자산 리스트 반환)
    def get_asset_by_id(self, asset_id):
        """
        자산의 고유 ID를 기준으로 자산을 조회하여 상세 정보를 반환
        :param asset_id: 자산의 고유 ID
        :return: 자산의 상세 정보 (asset_id, asset_type, description, price 등)
        """
        query_filter = {"_id": ObjectId(asset_id)}  # ObjectId로 변환
        asset_details = self.asset_collection.find_one(query_filter, {
            "name": 1,
            "asset_type": 1,
            "category": 1,
            "style": 1,
            "resolution": 1,
            "updated_at": 1,
            "particular_url": 1,
            "turnaround_url": 1,
            "rig_url": 1
        })
        
        if not asset_details:
            raise ValueError(f"Asset with ID {asset_id} not found.")
        
        # 각 URL 필드가 없을 경우 None으로 설정 (누락된 URL에 대한 기본값 처리)
        asset_details['particular_url'] = asset_details.get('particular_url', None)
        asset_details['turnaround_url'] = asset_details.get('turnaround_url', None)
        asset_details['rig_url'] = asset_details.get('rig_url', None)
        
        return asset_details

    # 데이터 수정 (Update)
    def update_asset(self, asset_id, update_data):
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
    def delete_asset(self, asset_id):
        """
        자산을 삭제합니다.
        :param asset_id: 삭제할 자산의 ID
        :return: 삭제 성공 여부 (True/False)
        """
        result = self.asset_collection.delete_one({"_id": ObjectId(asset_id)})  # 자산 ID를 기준으로 삭제
        return result.acknowledged  # 삭제 작업이 성공했으면 True, 실패하면 False 반환

    # 다운로드 수 증가 (Increment Download Count)
    def increment_download_count(self, asset_id):
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
