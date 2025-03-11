import sys, os
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from assetmanager import AssetService
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy
from db_crud import AssetDb  # 수정된 db_crud에서 Asset 클래스를 import


from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt


class AssetManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        
    def load_assets(self, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        """자산 데이터를 테이블에 로드"""
        assets = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip))
        self.display_assets(assets)
    
    def display_assets(self, assets):
        """자산을 UI 테이블에 표시"""
        max_columns = 5
        rows = (len(assets) // max_columns) + 1
        self.ui.tableWidget.setRowCount(rows)
        self.ui.tableWidget.setColumnCount(max_columns)
        
        for index, asset in enumerate(assets):
            row_index = index // max_columns
            col_index = index % max_columns
            self.add_thumbnail(row_index, col_index, asset)
    
    def add_thumbnail(self, row, col, asset):
        """자산 썸네일을 테이블에 추가"""
        thumbnail_path = asset["preview_url"]
        asset_name = asset["name"]
        asset_type = asset["asset_type"]
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setAlignment(Qt.AlignTop)
        
        thumbnail_label = QLabel()
        name_label = QLabel(asset_name)
        type_label = QLabel(asset_type)
        
        pixmap = QPixmap(thumbnail_path)
        thumbnail_label.setPixmap(pixmap)
        thumbnail_label.setFixedHeight(160)
        thumbnail_label.setAlignment(Qt.AlignCenter)
        
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        name_label.setFixedHeight(14)
        
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        type_label.setFixedHeight(18)
        
        layout.addWidget(thumbnail_label)
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        widget.setLayout(layout)
        
        self.ui.tableWidget.setCellWidget(row, col, widget)
        self.ui.tableWidget.resizeRowsToContents()


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
        asset_manager =   # Asset 클래스의 인스턴스를 생성
        return AssetDb().find(filter_conditions=filter_conditions, sort_by=sort_by, limit=limit, skip=skip)
            
    @staticmethod
    def get_asset_by_id(asset_id):
        """
        특정 ID의 자산 데이터를 가져옴.
        - UI에서 사용자가 클릭한 자산의 ID를 전달받아 해당 데이터를 조회
        """
        asset_manager = AssetDb()  # Asset 클래스의 인스턴스를 생성
        print (asset_id)
        return asset_manager.find_one(asset_id)
    
    @staticmethod
    def create_asset(asset_data):
        """
        새로운 자산 데이터를 생성하여 DB에 추가합니다.
        :param asset_data: 자산 데이터
        :return: 추가된 자산의 ID
        """
        asset_manager = AssetDb()  # AssetDb 클래스의 인스턴스를 생성
        return asset_manager.insert_one(asset_data)  # 자산 데이터를 DB에 삽입
    
    @staticmethod
    def update_asset(asset_id, update_data):
        """
        자산 데이터를 업데이트합니다.
        :param asset_id: 수정할 자산 ID
        :param update_data: 수정할 데이터
        :return: 업데이트 성공 여부
        """
        asset_manager = AssetDb()  # AssetDb 클래스의 인스턴스를 생성
        return asset_manager.update_one(asset_id, update_data)  # 자산 데이터 업데이트
    
    @staticmethod
    def delete_asset(asset_id):
        """
        자산 데이터를 삭제합니다.
        :param asset_id: 삭제할 자산 ID
        :return: 삭제 성공 여부
        """
        asset_manager = AssetDb()  # AssetDb 클래스의 인스턴스를 생성
        return asset_manager.delete_one(asset_id)  # 자산 삭제
    
    @staticmethod
    def update_count(asset_id):
        """
        자산 데이터를 업데이트합니다.
        :param asset_id: 수정할 자산 ID
        :param update_data: 수정할 데이터
        :return: 업데이트 성공 여부
        """
        asset_manager = AssetDb()  # AssetDb 클래스의 인스턴스를 생성
        return asset_manager.increment_count(asset_id)  # 자산 데이터 업데이트
    
    @staticmethod
    def search_asset(user_query):
        """
        데이터를 검색합니다.
        :param user_query: 검색어
        :return: 검색 성공 여부
        """
        asset_manager = AssetDb()  # AssetDb 클래스의 인스턴스를 생성
        return asset_manager.search(user_query)  # 자산 데이터 업데이트

