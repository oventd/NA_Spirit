# from pymongo import MongoClient

# client = MongoClient("mongodb://192.168.5.19:27017/")
# db = client["testdb"]
# print()
# print(db.list_collection_names())

# db = client["mydatabase"]
# collection = db["users"]

# # 데이터 조회
# print("모든 데이터 조회:")
# for user in collection.find():
#     print(user)



# 찾찾티비요
import pymongo  # MongoDB 작업을 위한 라이브러리

# MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB 서버에 연결
db = client["filter_test"]  # 사용할 데이터베이스 'filter_test'에 연결
asset_collection = db["test"]  # 'test'라는 컬렉션에 연결

# 특정 asset_id를 가진 문서 찾기
# asset = asset_collection.find_one({"asset_id": "362"})
asset = asset_collection.find({"asset_id"})

# 결과 출력
print(asset)

