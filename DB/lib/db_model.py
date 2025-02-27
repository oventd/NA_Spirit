from PySide6 import QtWidgets, QtCore
import sys
sys.path.append('/home/rapa/NA_Spirit/DB/lib')  # 사용자 지정 라이브러리 폴더 경로 추가
from lib.db_crud import *  # 절대 경로로 db_crud 모듈 임포트

class CustomTableModel(QtCore.QAbstractTableModel):
    """
    MongoDB 데이터를 처리하는 커스텀 테이블 모델
    """
    def __init__(self, data):
        super().__init__()
        self.user_data = data  # 데이터 저장
        # 데이터가 존재하면 첫 번째 데이터의 키(컬럼명)를 가져오고, 없으면 빈 리스트를 저장
        self.columns = list(self.user_data[0].keys()) if self.user_data else []
        self._data = data  # 데이터를 내부 변수로 저장

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
        self.beginResetModel()
        self.user_data = new_data  # 새로운 데이터 저장
        self.columns = list(self.user_data[0].keys()) if self.user_data else []
        self.endResetModel()

    def get_data(self):
        """
        데이터를 반환하는 메서드 수정
        """
        return self.user_data  # user_data를 반환하도록 수정
    
    

#     # def on_item_clicked(self, index):
#     #     """
#     #     사용자가 테이블에서 항목을 클릭했을 때 호출되는 함수
#     #     :param index: 클릭된 셀의 인덱스
#     #     """
#     #     clicked_row = index.row()  # 클릭된 행 번호
#     #     if clicked_row >= 0:
#     #         clicked_asset = self.user_data[clicked_row]  # 해당 행의 자산 데이터
#     #         asset_id = clicked_asset["_id"]  # _id를 통해 자산 식별
#     #         asset_details = find_one(asset_id)  # 자산 세부 정보 조회
#     #         print(asset_details)  # 예시: 세부 정보를 출력

