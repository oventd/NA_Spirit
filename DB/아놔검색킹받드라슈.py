import pymongo

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
    user_input = input("🔍 검색어를 입력하세요: ").strip()  # 사용자 입력 받기
    search_results = user_db.search(user_input)  # UserDb 인스턴스를 통해 search 호출

    # 검색 결과 출력
    if search_results:
        print("🔹 검색 결과:")
        for result in search_results:
            print(f"  - {result}")
    else:
        print("⚠️ 검색 결과가 없습니다.")