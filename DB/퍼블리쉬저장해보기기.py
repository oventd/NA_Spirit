import pymongo
from bson import ObjectId
from datetime import datetime
import sys
sys.path.append('/home/rapa/NA_Spirit/utils')
from json_utils import JsonUtils

class DbCrud:
    def __init__(self):
        # MongoDB 연결
        client = pymongo.MongoClient("mongodb://192.168.5.10:27017/")
        self.db = client["SpiritDatabase"]
        self.asset_collection = self.db["test"]  # 새로운 컬렉션에 저장해야 할지 여부는 데이터 구조에 따라 결정

    @classmethod
    def get_publish_data(cls):
        """JSON 데이터를 읽어옵니다."""
        print("[DEBUG] get_publish_settings() called")
        if cls._publish_settings is None:
            cls._publish_settings = JsonUtils.read_json("/home/rapa/NA_Spirit/DB/publish_data.json")
        print(f"[DEBUG] get_publish_settings() returns: {cls._publish_settings}")  # 디버깅용 출력
        return cls._publish_settings

    def upsert_asset(self, asset_data):
        """자산이 존재하면 수정하고, 존재하지 않으면 삽입합니다."""
        asset_name = asset_data.get('asset_name')
        asset_version = asset_data.get('version')

        # 수정할 데이터가 있으면 $set을 사용하여 새로운 필드를 추가하거나 수정합니다.
        asset_data["updated_at"] = datetime.utcnow()  # 수정 시간 업데이트

        # upsert=True를 사용하면 항목이 없으면 새로 삽입하고, 있으면 수정합니다.
        result = self.asset_collection.update_one(
            {"asset_name": asset_name, "version": asset_version},  # 검색 기준: asset_name과 version
            {"$set": asset_data},  # 필드가 없으면 추가되고, 있으면 수정됨
            upsert=True  # 데이터가 없으면 삽입, 있으면 수정
        )
        print(f"[DEBUG] Upsert result: {result.upserted_id if result.upserted_id else 'No new insert'}")
        return result

    def spirit_vfx_data(self):
        """파일 데이터를 삽입합니다."""
        publish_data = self.get_publish_data()  # JSON 데이터 읽기
        for item in publish_data:
            # 자산을 삽입하거나 수정하는 작업 수행
            self.upsert_asset(item)