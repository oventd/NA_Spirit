from pymongo import MongoClient

client = MongoClient("mongodb://192.168.5.19:27017/")
db = client["filter_test"]
collection = db["test"]

# # 데이터 삽입
# users = [
#     {"name": "Somi", "age": 211, "city": "Seoul"},
#     {"name": "Shin", "age": 312, "city": "Busan"},
#     {"name": "Charlie", "age": 251, "city": "Incheon"}
# ]
# collection.insert_many(users)
# print("데이터 삽입 완료!")

# 데이터 조회
print("모든 데이터 조회:")
for user in collection.find():
    print(user)

