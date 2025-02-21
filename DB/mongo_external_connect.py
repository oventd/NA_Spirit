from pymongo import MongoClient

client = MongoClient("mongodb://192.168.5.13:27017/")
db = client["mydatabase"]
collection = db["users"]

# 데이터 삽입
users = [
    {"name": "Alice", "age": 28, "city": "Seoul"},
    {"name": "Bob", "age": 32, "city": "Busan"},
    {"name": "Charlie", "age": 25, "city": "Incheon"}
]
collection.insert_many(users)
print("데이터 삽입 완료!")

# 데이터 조회
print("모든 데이터 조회:")
for user in collection.find():
    print(user)
