from PySide6 import QtWidgets, QtCore  # PySide6에서 QtWidgets와 QtCore 모듈 가져오기
from lib.db_crud import *  # 절대 경로로 db_crud 임포트
from lib.db_model import CustomTableModel  # 절대 경로로 db_model 임포트


class MainWindow(QtWidgets.QMainWindow):
    """
    필터 UI와 TableView를 통합 관리하는 메인 윈도우
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Asset Library")  # 윈도우 제목 설정
        self.setGeometry(100, 100, 800, 600)  # 윈도우 크기 및 위치 설정

        # 필터 UI 요소 생성
        self.checkbox_paid = QtWidgets.QCheckBox("Paid License")  # 유료 라이선스 체크박스
        self.checkbox_free = QtWidgets.QCheckBox("Free License")  # 무료 라이선스 체크박스
        self.checkbox_style = QtWidgets.QCheckBox("style")  # 스타일 체크박스
        self.checkbox_sort_downloads = QtWidgets.QCheckBox("Sort by Downloads")  # 다운로드 순 정렬 체크박스
        self.search_button = QtWidgets.QPushButton("Search")  # 검색 버튼

        # 테이블 뷰 생성
        self.table_view = QtWidgets.QTableView()
        self.model = CustomTableModel([])  # 초기 빈 데이터 모델 생성
        self.table_view.setModel(self.model)  # 테이블 뷰에 데이터 모델 설정

        # UI 레이아웃 설정
        filter_layout = QtWidgets.QVBoxLayout()  # 필터 UI를 위한 수직 레이아웃 생성
        filter_layout.addWidget(self.checkbox_paid)  # 유료 라이선스 체크박스 추가
        filter_layout.addWidget(self.checkbox_free)  # 무료 라이선스 체크박스 추가
        filter_layout.addWidget(self.checkbox_style)  # 스타일 체크박스 추가
        filter_layout.addWidget(self.checkbox_sort_downloads)  # 다운로드 순 정렬 체크박스 추가
        filter_layout.addWidget(self.search_button)  # 검색 버튼 추가

        main_layout = QtWidgets.QVBoxLayout()  # 메인 레이아웃 생성
        main_layout.addLayout(filter_layout)  # 필터 레이아웃 추가
        main_layout.addWidget(self.table_view)  # 테이블 뷰 추가

        central_widget = QtWidgets.QWidget()  # 중앙 위젯 생성
        central_widget.setLayout(main_layout)  # 중앙 위젯에 메인 레이아웃 설정
        self.setCentralWidget(central_widget)  # 메인 윈도우에 중앙 위젯 설정

        # 검색 버튼 클릭 시 필터 적용 함수 연결
        self.search_button.clicked.connect(self.apply_filter)

    @staticmethod
    def create_filter_conditions(filter_dict):
        """
        주어진 딕셔너리를 기반으로 필터 조건을 생성하는 팩토리 메서드
        """
        filter_conditions = {}
        for key, value in filter_dict.items():
            if isinstance(value, list):  # 리스트라면 '$in' 쿼리 적용
                filter_conditions[key] = {"$in": value}
            else:
                filter_conditions[key] = value
        return filter_conditions

    def apply_filter(self):
        """
        체크된 값만 필터 조건에 추가하여 MongoDB에서 데이터 조회
        """
        filter_dict = {}

        if self.checkbox_paid.isChecked():
            filter_dict.setdefault("license_type", []).append("Paid")
        if self.checkbox_free.isChecked():
            filter_dict.setdefault("license_type", []).append("Free")
        if self.checkbox_style.isChecked():
            filter_dict.setdefault("style", []).append("Stylized")

        # 다운로드 순으로 정렬할지 여부 확인
        sort_by_downloads = self.checkbox_sort_downloads.isChecked()
        # 다운로드 순으로 정렬하려면 'downloads' 필드 기준으로 정렬
        sort_by = "downloads" if sort_by_downloads else None        
        
        filter_conditions = self.create_filter_conditions(filter_dict)  # 팩토리 메서드 사용
        # 필터와 정렬 기준에 맞는 자산 조회
        assets = get_assets(filter_conditions, sort_by=sort_by, limit=20) 
        self.model.update_data(assets)  # 조회된 데이터를 테이블 모델에 적용


# Qt 애플리케이션 실행
def run_app():
    app = QtWidgets.QApplication([])  # QApplication 객체 생성 (애플리케이션 실행 준비)
    window = MainWindow()  # 메인 윈도우 객체 생성
    window.show()  # 메인 윈도우 표시
    app.exec_()  # 애플리케이션 실행 및 이벤트 루프 진입
