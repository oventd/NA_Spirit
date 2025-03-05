import pymongo
from bson import ObjectId  # MongoDB에서 사용하는 ObjectId를 처리하는 데 사용
class DbCrud:
    def __init__(self):
        # MongoDB 연결
        client = pymongo.MongoClient("mongodb://spirt:1234@localhost:27017/")
        self.db = client["filter_test"]
        self.asset_collection = self.db["test"]

    def search(self, user_query):
        """
        데이터에 대한 검색 기능을 수행합니다.
        :user_query: 검색할 데이터
        :return: 검색 결과
        """
        query = { "$text": { "$search": user_query } }
        projection = { "name": 1, "_id": 0, "score": { "$meta": "textScore" } }

        results = (
            self.asset_collection.find(query, projection)
            .sort([("score", {"$meta": "textScore"})])  # 정확도 순으로 정렬
            .limit(10)  # 최대 10개 제한
        )
        result_list = list(results)
        return result_list
    
    def sort_find(self, filter_conditions=None, sort_by=None, limit=40, skip=0, fields=None):
        """
        필터 조건에 맞는 자산들을 조회하고, 해당 자산들을 정렬합니다.
        :param filter_conditions: ObjectId 리스트 (기본값은 None, 모든 자산 조회)
        :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
        :param limit: 조회할 데이터 수 (기본값은 40)
        :param skip: 건너뛸 데이터 수 (기본값은 0)
        :param fields: 반환할 필드 목록 (기본값은 None, 특정 필드만 반환)
        :return: 조회된 자산 리스트
        """
        # filter_conditions가 None이면 빈 리스트로 초기화
        if filter_conditions is None:
            filter_conditions = []

        # ObjectId로 변환된 값들을 저장할 빈 리스트를 만들기
        object_ids = []

        # filter_conditions 리스트에 있는 각 값을 ObjectId로 변환하여 object_ids 리스트에 추가
        for value in filter_conditions:
            object_id = ObjectId(value)  # value를 ObjectId로 변환
            object_ids.append(object_id)  # 변환된 ObjectId를 리스트에 추가

        # _id 필드를 ObjectId 값들로 필터링하기 위한 쿼리 작성
        query_filter = {"_id": {"$in": object_ids}}

        # 필드 목록이 주어지면 그에 맞는 프로젝션 생성
        if fields:
            projection = {}  # 빈 딕셔너리 생성
            for field in fields:
                projection[field] = 1  # 각 필드를 1로 설정하여 포함시킴
        else:
            projection = None  # 필드가 없다면 None으로 설정

        
        # 파이프라인 생성
        pipeline = [
            {"$match": query_filter},  # _id 필터링
            {"$limit": limit},         # 제한된 개수만 조회
            {"$skip": skip},           # 건너뛰기
            {"$project": projection} if projection else None,  # 필드 선택
            {"$sort": {sort_by: pymongo.DESCENDING}} if sort_by else None,  # 정렬
        ]

        # None 값 제거 (필요한 단계만 파이프라인에 추가)
        pipeline = [step for step in pipeline if step]

        # 쿼리 실행
        result = list(self.asset_collection.aggregate(pipeline))
        
        return result


        

class UserDb(DbCrud):
    def __init__(self):
        super().__init__()  # 부모 클래스 생성자 호출
        self.setup_indexes()

    def setup_indexes(self):
        self.asset_collection.create_index([("name", "text"), ("description", "text")])  # 텍스트 인덱스 추가
        print("인덱스 설정 완료!")

    def search(self, user_query):
        """부모 클래스의 search()를 그대로 사용"""
        return super().search(user_query)


# 🔥 터미널에서 사용자 입력을 받음
if __name__ == "__main__":
    user_db = UserDb()  # UserDb의 인스턴스를 생성
    # user_input = input("🔍 검색어를 입력하세요: ").strip()  # 사용자 입력 받기
    # search_results = user_db.search(user_input)  # UserDb 인스턴스를 통해 search 호출

    # # 검색 결과 출력
    # if search_results:
    #     print("🔹 검색 결과:")
    #     for result in search_results:
    #         print(f"  - {result}")
    # else:
    #     print("⚠️ 검색 결과가 없습니다.")

    # 정렬 및 필터링된 조회
    filter_conditions = ["67bd6ea2e63d06c897d0de23", "67bd6ec57dbd058b9f0d999b", "67bd6ec57dbd058b9f0d999d"]  # 예시 ObjectId들
    sorted_results = user_db.sort_find(
        filter_conditions=filter_conditions, 
        sort_by="downloads",  # 다운로드 수 기준으로 정렬
        limit=3
    )

    # 정렬된 결과 출력
    if sorted_results:
        print("🔹 정렬된 검색 결과:")
        for result in sorted_results:
            print(f"  - {result}")
    else:
        print("⚠️ 정렬된 결과가 없습니다.")