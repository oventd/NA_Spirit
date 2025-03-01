from db_crud import UserDb  # 수정된 db_crud에서 Asset 클래스를 import


from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt

class ClickableLabel(QLabel):
    clicked = Signal()  # 클릭 시그널 생성

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 클릭 시그널 발생



class AssetService:
    """
    UI와 DB 사이의 중간 계층 역할을 수행하는 서비스 클래스.
    - UI에서는 직접 db_crud.py를 호출하지 않고, 이 클래스를 통해서만 데이터 요청을 함.
    """

    @staticmethod
    def get_all_assets(filter_conditions, sort_by, limit, skip): # 리뷰 메서드 이상함 all과 limit가 공존하는 이름 
        """
        모든 자산 데이터를 MongoDB에서 가져옴. 무한 스크롤을 지원.
        - db_crud.py의 find() 호출
        - 데이터를 UI에서 쉽게 사용 가능하도록 리스트로 변환
        :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
        :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
        :param limit: 조회할 데이터 수 (기본값은 5)
        :param skip: 건너뛸 데이터 수 (기본값은 0, 첫 번째 페이지)
        :return: 조회된 자산 리스트
        """
        asset_manager = UserDb()  # Asset 클래스의 인스턴스를 생성
        return asset_manager.find(filter_conditions=filter_conditions, sort_by=sort_by, limit=limit, skip=skip)

    @staticmethod
    def get_asset_by_id(asset_id):
        """
        특정 ID의 자산 데이터를 가져옴.
        - UI에서 사용자가 클릭한 자산의 ID를 전달받아 해당 데이터를 조회
        """
        asset_manager = UserDb()  # Asset 클래스의 인스턴스를 생성
        print (asset_id)
        return asset_manager.find_one(asset_id)
    
    @staticmethod
    def create_asset(asset_data):
        """
        새로운 자산 데이터를 생성하여 DB에 추가합니다.
        :param asset_data: 자산 데이터
        :return: 추가된 자산의 ID
        """
        asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
        return asset_manager.insert_one(asset_data)  # 자산 데이터를 DB에 삽입
    
    @staticmethod
    def update_asset(asset_id, update_data):
        """
        자산 데이터를 업데이트합니다.
        :param asset_id: 수정할 자산 ID
        :param update_data: 수정할 데이터
        :return: 업데이트 성공 여부
        """
        asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
        return asset_manager.update_one(asset_id, update_data)  # 자산 데이터 업데이트
    
    @staticmethod
    def delete_asset(asset_id):
        """
        자산 데이터를 삭제합니다.
        :param asset_id: 삭제할 자산 ID
        :return: 삭제 성공 여부
        """
        asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
        return asset_manager.delete_one(asset_id)  # 자산 삭제
    
    @staticmethod
    def update_count(asset_id):
        """
        자산 데이터를 업데이트합니다.
        :param asset_id: 수정할 자산 ID
        :param update_data: 수정할 데이터
        :return: 업데이트 성공 여부
        """
        asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
        return asset_manager.increment_count(asset_id)  # 자산 데이터 업데이트
    
    @staticmethod
    def search_asset(user_query):
        """
        데이터를 검색합니다.
        :param user_query: 검색어
        :return: 검색 성공 여부
        """
        asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
        return asset_manager.search(user_query)  # 자산 데이터 업데이트


# from lib.db_crud import UserDb  # 수정된 db_crud에서 Asset 클래스를 import

# class AssetService:
#     """
#     UI와 DB 사이의 중간 계층 역할을 수행하는 서비스 클래스.
#     - UI에서는 직접 db_crud.py를 호출하지 않고, 이 클래스를 통해서만 데이터 요청을 함.
#     """

#     @staticmethod
#     def get_all_assets(filter_conditions=None, sort_by=None, limit=40, skip=0):
#         """
#         모든 자산 데이터를 MongoDB에서 가져옴. 무한 스크롤을 지원.
#         - db_crud.py의 find() 호출
#         - 데이터를 UI에서 쉽게 사용 가능하도록 리스트로 변환
#         :param filter_conditions: 필터 조건 (기본값은 None, 모든 자산 조회)
#         :param sort_by: 정렬 기준 (기본값은 None, 정렬하지 않음)
#         :param limit: 조회할 데이터 수 (기본값은 5)
#         :param skip: 건너뛸 데이터 수 (기본값은 0, 첫 번째 페이지)
#         :return: 조회된 자산 리스트
#         """
#         asset_manager = UserDb()  # Asset 클래스의 인스턴스를 생성
#         return asset_manager.find(filter_conditions=filter_conditions, sort_by=sort_by, limit=limit, skip=skip)

#     @staticmethod
#     def get_asset_by_id(object_id):
#         """
#         특정 ID의 자산 데이터를 가져옴.
#         - UI에서 사용자가 클릭한 자산의 ID를 전달받아 해당 데이터를 조회
#         """
#         asset_manager = UserDb()  # Asset 클래스의 인스턴스를 생성
#         return asset_manager.find_one(object_id)
    
#     @staticmethod
#     def create_asset(asset_data):
#         """
#         새로운 자산 데이터를 생성하여 DB에 추가합니다.
#         :param asset_data: 자산 데이터
#         :return: 추가된 자산의 ID
#         """
#         asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
#         return asset_manager.insert_one(asset_data)  # 자산 데이터를 DB에 삽입
    
#     @staticmethod
#     def update_asset(asset_id, update_data):
#         """
#         자산 데이터를 업데이트합니다.
#         :param asset_id: 수정할 자산 ID
#         :param update_data: 수정할 데이터
#         :return: 업데이트 성공 여부
#         """
#         asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
#         return asset_manager.update_one(asset_id, update_data)  # 자산 데이터 업데이트
    
#     @staticmethod
#     def delete_asset(asset_id):
#         """
#         자산 데이터를 삭제합니다.
#         :param asset_id: 삭제할 자산 ID
#         :return: 삭제 성공 여부
#         """
#         asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
#         return asset_manager.delete_one(asset_id)  # 자산 삭제
    
#     @staticmethod
#     def update_count(asset_id):
#         """
#         자산 데이터를 업데이트합니다.
#         :param asset_id: 수정할 자산 ID
#         :param update_data: 수정할 데이터
#         :return: 업데이트 성공 여부
#         """
#         asset_manager = UserDb()  # UserDb 클래스의 인스턴스를 생성
#         return asset_manager.increment_count(asset_id)  # 자산 데이터 업데이트

