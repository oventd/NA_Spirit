from datetime import datetime, timedelta
import pymongo
from bson import ObjectId  # MongoDB의 ObjectId 처리용

# 1️⃣ MongoDB 연결
client = pymongo.MongoClient("mongodb://spirt:1234@localhost:27017/")
db = client["filter_test"]
asset_collection = db["test"]

# # 1️⃣ 모든 인덱스 삭제
# asset_collection.drop_indexes()
# print("✅ 모든 인덱스 삭제 완료")

# # 2️⃣ 삭제 후 인덱스 목록 확인
# indexes = asset_collection.index_information()
# print("📌 현재 인덱스 목록:")
# for index_name, index_info in indexes.items():
#     print(f"🔹 {index_name}: {index_info}")

# 2️⃣ 텍스트 인덱스 생성 (이미 생성되었으면 실행 시 오류 발생 가능)
# try:
#     asset_collection.create_index([("name", "text"), ("description", "text")])
#     print("✅ 텍스트 인덱스 생성 완료")
# except Exception as e:
#     print(f"⚠️ 텍스트 인덱스 생성 오류: {e}")
# try:
#     asset_collection.create_index([("category", "text"), ("style", "text")])
#     print("✅ 텍스트 인덱스 생성 완료")
# except Exception as e:
#     print(f"⚠️ 텍스트 인덱스 생성 오류: {e}")


# 3️⃣ 검색 함수
def search():
    print("🔎 search() 메서드 시작")  # 실행 여부 확인


    # sample_data = asset_collection.find({"$text": {"$search": "metal"}})
    # for item in sample_data:
    #     print(item)


    query = { "$text": { "$search": "Realistic" } }
    projection = { "name": 1, "_id": 0 }  # name 필드만 가져옴 (_id는 제외)

    try:
        results = asset_collection.find(query, projection).limit(10)
        print("🔎 검색 수행 완료")  # 쿼리 실행 확인
        result_list = list(results)  # 리스트 변환 후 반환

        if result_list:
            print("🔹 검색 결과:")
            for doc in result_list:
                print(f"  - {doc}")
        else:
            print("⚠️ 검색 결과가 없습니다.")
        return result_list
    except Exception as e:
        print(f"⚠️ search() 메서드 오류: {e}")
        return []



indexes = asset_collection.index_information()
print("📌 현재 인덱스 목록:")
for index_name, index_info in indexes.items():
    print(f"🔹 {index_name}: {index_info}")

# 4️⃣ 검색 실행
search()
