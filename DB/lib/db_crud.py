import pymongo  # MongoDB와의 연결을 위한 라이브러리
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용
import random

# MongoDB 연결
client = pymongo.MongoClient("mongodb://spirt:1234@localhost:27017/")  # 로컬 MongoDB 서버에 연결
db = client["filter_test"]  # 사용할 데이터베이스 'filter_test'에 연결
asset_collection = db["test"]  # 'test'라는 컬렉션에 연결
print("Database connected")  # 연결 성공 메시지 출력

# **인덱스 생성 (단일 인덱스 추가)**
# 'file_format'에 대한 단일 인덱스 생성
asset_collection.create_index([("file_format", pymongo.ASCENDING)])

# 'creator'에 대한 단일 인덱스 생성
asset_collection.create_index([("creator", pymongo.ASCENDING)])

# 'updated_at'에 대한 단일 인덱스 생성
asset_collection.create_index([("updated_at", pymongo.DESCENDING)])

# 'downloads'와 'statistics.downloads'는 동일한 의미를 가지므로 하나의 인덱스로 처리 가능
asset_collection.create_index([("downloads", pymongo.DESCENDING)])


# 데이터 삽입 (Create)
def insert_asset(asset_data):
    """
    새로운 자산 데이터를 컬렉션에 삽입합니다.
    :asset_data: 삽입할 자산 데이터 (사전 형태로 전달)
    :return: 삽입된 자산의 ID (문자열 형태)
    """
    # 자산 생성 시간과 수정 시간을 UTC로 추가 (시간대에 상관없는 시간 저장)
    asset_data["created_at"] = datetime.utcnow()  # 생성 시간 추가
    asset_data["updated_at"] = datetime.utcnow()  # 수정 시간 추가
    result = asset_collection.insert_one(asset_data)  # asset_data를 MongoDB 컬렉션에 삽입
    return str(result.inserted_id)  # 삽입된 자산의 고유 ID를 반환

# 데이터 조회 (Read)
def get_assets(filter_conditions=None, sort_by=None, limit=10):
    """
    필터 조건에 맞는 자산들을 조회합니다.
    :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
    :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
    :param limit: 조회할 데이터 수 (기본값은 10)
    :return: 조회된 자산 리스트
    """
    if filter_conditions is None:
        filter_conditions = {}  # 필터 조건이 없으면 모든 자산을 조회

    # 리스트 값이 있는 필터 조건을 자동으로 $in 변환 (리스트 값에 맞는 자산만 조회)
    query_filter = {}
    for key, value in filter_conditions.items():
        if isinstance(value, list):  # 값이 리스트라면 $in 조건 사용
            query_filter[key] = {"$in": value}
        else:  # 값이 리스트가 아니면 그냥 그 값으로 조회
            query_filter[key] = value

    # 필터 조건에 맞는 자산을 조회
    query = asset_collection.find(query_filter)
    
    if sort_by:
        # sort_by 값이 주어지면, 해당 필드를 기준으로 정렬
        # 예를 들어 'downloads'라면 다운로드 수 기준으로 내림차순 정렬
        query = query.sort(sort_by, pymongo.DESCENDING)

    # 조회할 자산 수를 limit으로 제한하고 리스트로 반환
    return list(query.limit(limit))


# 특정 자산 조회 (ID로 조회)
def get_asset_by_id(asset_id):
    """
    자산 ID를 기준으로 자산을 조회합니다.
    :param asset_id: 자산의 ID (문자열로 입력)
    :return: 자산 데이터 (자산이 존재하지 않으면 None)
    """
    return asset_collection.find_one({"_id": ObjectId(asset_id)})  # 자산 ID를 기준으로 자산을 조회

# 데이터 수정 (Update)
def update_asset(asset_id, update_data):
    """
    기존 자산 데이터를 수정합니다. 만약 자산이 없으면 새로 생성합니다.
    :param asset_id: 수정할 자산의 ID
    :param update_data: 수정할 데이터 (사전 형태)
    :return: 수정 성공 여부 (True/False)
    """
    update_data["updated_at"] = datetime.utcnow()  # 수정 시간을 현재 시간으로 업데이트
    # 자산 ID를 기준으로 해당 자산을 업데이트 (자산이 없으면 새로 생성)
    result = asset_collection.update_one(
        {"_id": ObjectId(asset_id)},  # 자산 ID로 검색
        {"$set": update_data},  # 수정할 데이터 설정
        upsert=True  # 자산이 없으면 새로 생성
    )
    return result.acknowledged  # 수정 작업이 성공했으면 True, 실패하면 False 반환

# 데이터 삭제 (Delete)
def delete_asset(asset_id):
    """
    자산을 삭제합니다.
    :param asset_id: 삭제할 자산의 ID
    :return: 삭제 성공 여부 (True/False)
    """
    result = asset_collection.delete_one({"_id": ObjectId(asset_id)})  # 자산 ID를 기준으로 삭제
    return result.acknowledged  # 삭제 작업이 성공했으면 True, 실패하면 False 반환

# 다운로드 수 증가 (Increment Download Count)
def increment_download_count(asset_id):
    """
    자산의 다운로드 수를 증가시킵니다.
    :param asset_id: 다운로드 수를 증가시킬 자산의 ID
    :return: 다운로드 수 증가 여부 (True/False)
    """
    result = asset_collection.update_one(
        {"_id": ObjectId(asset_id)},  # 자산 ID로 자산 찾기
        {"$inc": {"statistics.downloads": 1}},  # 다운로드 수 1 증가
    )
    return result.modified_count > 0  # 다운로드 수가 증가했으면 True 반환

# 애플리케이션 종료 시 연결 종료
client.close()


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


"""랜덤 데이터 생성 ㅎ"""
# 자산 데이터를 생성하는 함수
# def generate_asset_data():
#     """
#     자산 데이터를 생성하는 함수
#     :return: 자산 데이터 (사전 형태)
#     """
#     asset_types = ["3D Model", "Material", "Texture", "HDRI"]
#     categories = ["Environment", "Character", "Props", "Vehicle", "Weapon", "Architecture", "Others"]
#     styles = ["Realistic", "Stylized", "Procedural"]
#     resolutions = ["Low-poly", "Medium-poly", "High-poly"]
#     file_formats = ["ALL", "SBSAR", "SBS", "FBX", "GLB", "EXR", "HDRI"]
#     license_types = ["Paid", "Free"]
#     creator_names = ["John Doe", "Alice Smith", "Bob Johnson", "Eva White", "Charlie Brown", 
#                      "David Lee", "Mia Garcia", "Liam Scott", "Sophia King", "James Turner"]
    
#     asset_data = {
#         "_id": f"{random.randint(100000000000000000000000000, 999999999999999999999999999)}",  # Random ObjectId-like string
#         "asset_id": f"{random.randint(1, 1000):03d}",
#         "name": f"Asset {random.randint(1, 100)}",
#         "description": f"A description for asset {random.randint(1, 100)}",
#         "thumbnail_url": f"http://example.com/thumbnail{random.randint(1, 100)}.jpg",
#         "preview_url": f"http://example.com/preview{random.randint(1, 100)}.jpg",
#         "asset_type": random.choice(asset_types),
#         "category": random.choice(categories),
#         "style": random.choice(styles),
#         "resolution": random.choice(resolutions),
#         "file_format": random.choice(file_formats),
#         "size": f"{random.randint(1, 500)}MB",
#         "license_type": random.choice(license_types),
#         "price": random.randint(0, 100),
#         "creator_id": f"{random.randint(1000, 9999)}",
#         "creator_name": random.choice(creator_names),  # 랜덤으로 creator_name 선택
#         "downloads": random.randint(50, 1000),
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }
    
#     return asset_data
# # 자산 데이터 20개 생성 후 MongoDB에 삽입
# assets_data = [generate_asset_data() for _ in range(20)]  # 20개 자산 데이터 생성

# # 자산 데이터를 MongoDB에 삽입
# for asset in assets_data:
#     insert_asset(asset)  # 자산 데이터를 DB에 삽입

# print("20개의 자산 데이터가 MongoDB에 성공적으로 삽입되었습니다.")