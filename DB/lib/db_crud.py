# pymongo와 ObjectId, datetime 모듈을 임포트합니다.
import pymongo  # MongoDB와의 연결을 위한 라이브러리
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
from datetime import datetime  # 현재 날짜와 시간을 다룰 때 사용

# MongoDB 연결
client = pymongo.MongoClient("mongodb://spirt:1234@localhost:27017/")  # 로컬 MongoDB 서버에 연결
db = client["filter_test"]  # 사용할 데이터베이스 'filter_test'에 연결
asset_collection = db["test"]  # 'test'라는 컬렉션에 연결
print("Database connected")  # 연결 성공 메시지 출력

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
        # sort_by 값이 주어지면, 해당 필드를 기준으로 내림차순 정렬
        query = query.sort(sort_by, pymongo.DESCENDING)

    # 조회할 자산 수를 limit로 제한하고 리스트로 반환
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
    :return: 수정된 문서의 개수 (다운로드 수가 증가된 자산의 수)
    """
    # 자산의 다운로드 수를 1 증가시킴
    result = asset_collection.update_one(
        {"_id": ObjectId(asset_id)},  # 자산 ID로 자산 찾기
        {"$inc": {"statistics.downloads": 1}},  # 'statistics.downloads' 필드를 1 증가
    )
    return result.modified_count  # 다운로드 수가 수정된 자산의 개수 반환

# 사용 예시 (주석 처리된 코드)
# filter_conditions = {'file_format': 'OBJ', 'creator_name': 'Jane Smith'}
# assets = get_assets(filter_conditions=filter_conditions, sort_by="downloads", limit=5)
# for asset in assets:
#     print(asset)
