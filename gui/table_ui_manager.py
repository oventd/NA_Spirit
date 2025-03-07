# 로거 파일 추가해서 유저가 중요한 
##### json 파일은 나스피릿에 넣고 이그노어 에 포함

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget,QGraphicsOpacityEffect
from PySide6.QtCore import QFile, Qt, Signal, QEvent, QObject, QUrl
from PySide6.QtGui import QPixmap, QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy ,QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from functools import partial
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
from asset_service import ClickableLabel

from PySide6.QtCore import QObject, QEvent, Qt
from constant import *
# from add_video_player import *
from subwin_ui_manager import SubWinUiManager


class TableUiManager:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TableUiManager, cls).__new__(cls)

        return cls._instance

    def __init__(self,ui):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            self.ui = ui
            self.ui.comboBox.currentTextChanged.connect(self.set_sorting_option)
            self._initialized = True  # 인스턴스가 초기화되었음을 표시

    def set_sorting_option(self, option):
            #유저가 설정한 sorting_option에 맞게 table에 적절한 인자를 전달하여 테이블 위젯의 나열순서를 정함
            if option == "오래된 순":
                print(f"오래된 순의 필터임 :{self.check_dict}")
                self.table_widget(self.check_dict,UPDATED_AT, 40, 0,None)

            elif option =="다운로드 순":
                print("다운로드된 순서를 정렬할게요")
                self.table_widget(self.check_dict,DOWNLOADS, 40, 0,None)

            else:
                print("최신 순서를 정렬할게요")
                self.table_widget(self.check_dict,CREATED_AT, 40, 0, None)
    @staticmethod
    def table_widget(ui, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        # 리뷰 이거 셀프로 init에 구현 이거 근데 저장하는 변수명이 쫌...... 
        # 리뷰 static밖에 없는데 왜 객체 생성????
        ui.like_empty_notice.hide()
    
        asset = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip)) # 모두 가져올거기 때문에 filter_conditions 는 빈딕셔너리
        print(f"asset입니다 >>>>>>> {asset}")
        TableUiManager.make_table(ui,asset)
    @staticmethod
    def make_table(ui, asset):
        len_asset =len(asset)
        ui.tableWidget.horizontalHeader().setVisible(False)  # 열(가로) 헤더 숨기기
        ui.tableWidget.verticalHeader().setVisible(False)  # 행(세로) 헤더 숨기기

        max_columns = 5  # 한 줄에 최대 5개 배치

        rows = (len_asset / max_columns +1)   # 행 개수 계산

        ui.tableWidget.setRowCount(rows)  # 행 개수 설정
        ui.tableWidget.setColumnCount(max_columns)  # 열 개수 설정

        for index, asset in enumerate(asset):
            row_index = index // max_columns  # index 항목이 몇 번째 행(row)에 있는 정의
            col_index = index % max_columns   # 나머지를 통해 몇번째 열에 있는지 정의
            TableUiManager.add_thumbnail(ui,row_index, col_index, asset)
    @staticmethod
    def add_thumbnail(ui, row, col, asset):
        subwin_ui_manager = SubWinUiManager(ui)
        thumbnail_path = asset["preview_url"]
        asset_name = asset["name"] 
        aseet_type = asset["asset_type"]

        widget = QWidget()  # 셀 안에 넣을 위젯 생성
        layout = QVBoxLayout()  # 세로 정렬을 위한 레이아웃 생성
        layout.setContentsMargins(0, 0, 0, 10)  # 여백 제거
        layout.setAlignment(Qt.AlignTop)

        #asset[]#여기에 찾을 항목 적어서 값 도출  

        Thum = ClickableLabel("썸네일", parent=widget)
        name = ClickableLabel("이름", parent=widget)
        type = ClickableLabel("타입", parent=widget)

        Thum.clicked.connect(lambda: subwin_ui_manager.del_label(asset))
        name.clicked.connect(lambda: subwin_ui_manager.del_label(asset))
        type.clicked.connect(lambda: subwin_ui_manager.del_label(asset))

        layout.addWidget(Thum)
        layout.addWidget(name)
        layout.addWidget(type)

        widget.setLayout(layout)  # 위젯에 레이아웃 설정

        # 리뷰 엔터 개 길어


        pixmap = QPixmap(thumbnail_path)
        if pixmap.isNull():
            print(f" 이미지 로드 실패: {thumbnail_path}")

        Thum.setPixmap(pixmap)
        Thum.setFixedHeight(160)

        
        Thum.setAlignment(Qt.AlignCenter)
        


        name.setText(asset_name)
        name.setAlignment(Qt.AlignCenter)
        type.setText(aseet_type)

        name.setStyleSheet("""
            color: white;                 /* 글자 색상 */
            font-family: 'Pretendard';          /* 글꼴 */
            font-size: 14px;              /* 글자 크기 */
            font-weight: Thin;            /* 글자 굵기 */
        """)


        name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        name.setFixedHeight(14)
        name.setAlignment(Qt.AlignCenter)

        type.setStyleSheet("color: white;")
        type.setStyleSheet("""
            color: white;                 /* 글자 색상 */
            font-family: 'Pretendard';          /* 글꼴 */
            font-size: 12px;              /* 글자 크기 */
            font-weight: Pretendard-ExtraLight;            /* 글자 굵기 */
        """)
        type.setAlignment(Qt.AlignCenter)
        
        type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        type.setFixedHeight(18)

        ui.tableWidget.setCellWidget(row, col, widget)  # 행과 열에 이미지 추가
        ui.tableWidget.resizeRowsToContents() 