from PySide6 import QtWidgets, QtCore  # PySide6에서 QtWidgets와 QtCore 모듈 가져오기
import sys
import os
# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)
from asset_service import AssetService  # AssetService 임포트
from db_model import CustomTableModel  # 절대 경로로 db_model 임포트

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
        self.checkbox_style = QtWidgets.QCheckBox("Stylized")  # 스타일 체크박스
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

        # 테이블 뷰에서 클릭된 자산에 대한 세부 정보 조회 함수 연결
        self.table_view.clicked.connect(self.on_item_clicked)

    @staticmethod
    def create_filter_conditions(filter_dict):
        """
        주어진 딕셔너리를 기반으로 필터 조건을 생성하는 팩토리 메서드

        :filter_dict: 필터 적용의 딕셔너리 자료형
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
        sort_by = "downloads" if sort_by_downloads else None        

        filter_conditions = self.create_filter_conditions(filter_dict)
        print(f"Filter conditions in apply_filter: {filter_conditions}")  # ✅ 필터 조건 확인

        if not filter_conditions:
            filter_conditions = {}  # 기본적으로 빈 딕셔너리 할당

        # 🚀 필터를 적용해서 데이터 가져오기
        assets = AssetService.get_all_assets(filter_conditions=filter_conditions, sort_by=sort_by)  # ✅ 필터 반영

        # 데이터 확인
        if not assets:
            print("No assets found")  # 데이터가 없는 경우 확인
        else:
            print(f"Fetched assets in apply_filter: {assets}")  # ✅ 필터링된 데이터 확인

        self.model.update_data(assets)  # ✅ UI 테이블 데이터 업데이트
        print(f"Data after update: {self.model.get_data()}")  # ✅ 디버깅용 데이터 출력



    def on_item_clicked(self, index):
        """
        자산 ID를 클릭했을 때 자산의 상세 정보를 조회하는 함수
        """
        clicked_row = index.row()  # 클릭된 행 번호
        data_length = len(self.model.get_data())  # 데이터 길이

        # 데이터가 비어있는지 확인
        if clicked_row < 0 or clicked_row >= data_length:
            print(f"Invalid row index: {clicked_row}. Data length: {data_length}")
            return  # 유효하지 않은 인덱스일 경우 처리

        clicked_asset = self.model.get_data()[clicked_row]  # 해당 행의 자산 데이터
        asset_id = clicked_asset['_id']  # 자산의 고유 ID를 가져옴

        try:
            # 자산 고유 ID로 세부 정보 조회
            asset_details = AssetService.get_asset_by_id(asset_id)  # AssetService를 통해 자산 세부 정보 조회
            self.show_asset_details(asset_details)  # 자산 상세 정보 UI에 표시
        except ValueError as e:
            print(f"Error: {e}")  # 오류 메시지 출력
            # UI에서 오류 메시지를 표시하거나, 사용자에게 알려줄 방법을 추가할 수 있음

    def show_asset_details(self, asset_details):
        """
        자산 세부 정보를 표시하는 함수
        """
        print(f"Asset details: {asset_details}")  # 디버깅용 로그 추가

        if not asset_details:
            print("Error: No asset details found.")
            return  # 자산 세부 정보가 없으면 함수 종료

        details_window = QtWidgets.QWidget()
        details_window.setWindowTitle("Asset Details")
        details_layout = QtWidgets.QVBoxLayout()

        # Asset ID 출력
        asset_id_label = QtWidgets.QLabel(f"Asset ID: {asset_details.get('asset_id', 'N/A')}")
        details_layout.addWidget(asset_id_label)

        # Asset Type 출력
        asset_type_label = QtWidgets.QLabel(f"Asset Type: {asset_details.get('asset_type', 'N/A')}")
        details_layout.addWidget(asset_type_label)

        # Description 출력
        description_label = QtWidgets.QLabel(f"Description: {asset_details.get('description', 'N/A')}")
        details_layout.addWidget(description_label)

        # Price 출력
        price_label = QtWidgets.QLabel(f"Price: {asset_details.get('price', 'N/A')}")
        details_layout.addWidget(price_label)

        details_window.setLayout(details_layout)
        details_window.show()



# Qt 애플리케이션 실행
def run_app():
    app = QtWidgets.QApplication([])  # QApplication 객체 생성 (애플리케이션 실행 준비)
    window = MainWindow()  # 메인 윈도우 객체 생성
    window.show()  # 메인 윈도우 표시
    app.exec_()  # 애플리케이션 실행 및 이벤트 루프 진입
