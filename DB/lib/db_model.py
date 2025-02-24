from PySide6 import QtWidgets, QtCore  # PySide6에서 QtWidgets와 QtCore 모듈 가져오기
import sys  # 시스템 관련 모듈
sys.path.append('/home/rapa/NA_Spirit/DB/lib')  # 사용자 지정 라이브러리 폴더 경로 추가
from db_crud import *  # db_crud 모듈의 모든 함수와 클래스 가져오기

class CustomTableModel(QtCore.QAbstractTableModel):
    """
    MongoDB 데이터를 처리하는 커스텀 테이블 모델
    """
    def __init__(self, data):
        super().__init__()
        self.user_data = data  # 데이터 저장
        # 데이터가 존재하면 첫 번째 데이터의 키(컬럼명)를 가져오고, 없으면 빈 리스트를 저장
        self.columns = list(self.user_data[0].keys()) if self.user_data else []

    def rowCount(self, *args, **kwargs):
        # 데이터 행(row)의 개수를 반환
        return len(self.user_data)

    def columnCount(self, *args, **kwargs):
        # 데이터 열(column)의 개수를 반환
        return len(self.columns)

    def data(self, index, role):
        """
        특정 셀의 데이터를 반환하는 함수
        """
        if role == QtCore.Qt.DisplayRole:  # 화면에 표시할 데이터 요청 시 실행
            row = self.user_data[index.row()]  # 선택한 행의 데이터 가져오기
            column = self.columns[index.column()]  # 선택한 열의 키 가져오기
            return str(row[column])  # 문자열로 변환하여 반환
        return None  # 그 외의 경우에는 None 반환

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        테이블 헤더(컬럼명) 반환
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section]  # 컬럼명 반환

    def update_data(self, new_data):
        """
        새로운 데이터로 테이블을 갱신하는 함수
        """
        self.beginResetModel()  # 데이터 변경 시작을 알림
        self.user_data = new_data  # 새로운 데이터 저장
        self.columns = list(self.user_data[0].keys()) if self.user_data else []  # 컬럼명 갱신
        self.endResetModel()  # 데이터 변경 완료를 알림


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
        self.checkbox_style = QtWidgets.QCheckBox("style")  # 무료 라이선스 체크박스
        self.search_button = QtWidgets.QPushButton("Search")  # 검색 버튼

        # 테이블 뷰 생성
        self.table_view = QtWidgets.QTableView()
        self.model = CustomTableModel([])  # 초기 빈 데이터 모델 생성
        self.table_view.setModel(self.model)  # 테이블 뷰에 데이터 모델 설정

        # UI 레이아웃 설정
        filter_layout = QtWidgets.QVBoxLayout()  # 필터 UI를 위한 수직 레이아웃 생성
        filter_layout.addWidget(self.checkbox_paid)  # 유료 라이선스 체크박스 추가
        filter_layout.addWidget(self.checkbox_free)  # 무료 라이선스 체크박스 추가
        filter_layout.addWidget(self.checkbox_style)  # 무료 라이선스 체크박스 추가
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

        filter_conditions = self.create_filter_conditions(filter_dict)  # 팩토리 메서드 사용
        assets = get_assets(filter_conditions, limit=10)  # 필터 조건에 맞는 데이터 조회 (최대 10개)
        self.model.update_data(assets)  # 조회된 데이터를 테이블 모델에 적용


# Qt 애플리케이션 실행
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # QApplication 객체 생성 (애플리케이션 실행 준비)
    window = MainWindow()  # 메인 윈도우 객체 생성
    window.show()  # 메인 윈도우 표시
    sys.exit(app.exec_())  # 애플리케이션 실행 및 이벤트 루프 진입