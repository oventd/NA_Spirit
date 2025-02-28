import pymongo
from pymongo.errors import ConnectionFailure
import threading
from db_constant import MONGODB_ADRESS, DATA_BASE

class MongoDBClient:
    _client = None
    _db = None
    _lock = threading.Lock()  # 멀티스레드 환경에서의 동시 접근을 방지

    @classmethod
    def get_client(cls):
        """
        MongoDB 클라이언트를 싱글턴 방식으로 반환
        이미 클라이언트가 존재하면 재사용
        """
        if cls._client is None:
            with cls._lock:  # 멀티스레드 환경에서의 동시 접근을 방지
                if cls._client is None:  # 이중 검사 (double-checked locking)
                    try:
                        # 커넥션 풀의 최대, 최소 연결 수를 지정함(메모리 절약을 위한 것임)
                        cls._client = pymongo.MongoClient(MONGODB_ADRESS, maxPoolSize=50, minPoolSize=5)
                        print("MongoDB client created and connected successfully.")
                    except ConnectionFailure as e:
                        print(f"MongoDB connection failed: {e}")
                        raise
        return cls._client

    @classmethod
    def get_db(cls):
        """데이터베이스 인스턴스를 반환"""
        if cls._db is None:
            cls.get_client()  # 클라이언트를 먼저 확보한 뒤
            cls._db = cls._client[DATA_BASE]  # 데이터베이스 선택 (filter_test)
        return cls._db

    @classmethod
    def close_connection(cls):
        """MongoDB 클라이언트를 종료 (애플리케이션 종료 시 호출 가능)"""
        if cls._client:
            cls._client.close()
            print("MongoDB connection closed.")
            cls._client = None
            cls._db = None