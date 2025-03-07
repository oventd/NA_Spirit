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

from tree_ui_manager import TreeUiManager
from table_ui_manager import TableUiManager
from subwin_ui_manager import SubWinUiManager

from like_state import LikeState

class DefaultUiManager:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DefaultUiManager, cls).__new__(cls)

        return cls._instance
    
    def __init__(self, ui, image_labels):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            super().__init__()
            self.ui = ui
            self.image_labels = image_labels
            self.main_ui_setting()
            self._initialized = True  # 인스턴스가 초기화되었음을 표시
    def make_label_list(self): 
        for _ in range(4):  # 4개의 QLabel을 미리 생성
            label = QLabel()
            label.setFixedSize(60, 60)
            label.setAlignment(Qt.AlignCenter)
            self.ui.image_widget_s.addWidget(label)  # 초기 레이아웃에 QLabel 추가
            self.image_labels.append(label)



   

    def set_search_area_design(self):
        search_input =self. ui.search
        search_input.setPlaceholderText("검색하기") 
        search_input.setStyleSheet("""
        QLineEdit {
            border: none;                  /* 테두리 제거 */
            background: transparent;       /* 배경을 투명으로 설정 */
            color: white;                  /* 글자 색상을 흰색으로 설정 */
            font-family: 'Pretendard';     /* 폰트는 Pretendard로 설정 */
            font-weight: light;            /* 폰트 두께를 light로 설정 */
            font-size: 13px;               /* 폰트 크기는 11px */
        }
    """)
        
    def main_ui_setting(self):

        """
        메인 UI 설정
        - 토글 버튼의 toggle의 디폴트 상태를 인스턴스 변수로 정의한다.
        - 토글 버튼에 토글 이미지를 설정/ 디폴트 이미지는 toggle_open.png
        - 메인 ui의 이미지 bg.png 배경으로 설정
        """

        self.sub_bar = False
        
        self.user_num()
        self.make_label_list()
        TreeUiManager.tree_widget(self.ui)
        TableUiManager.table_widget(self.ui,None,UPDATED_AT, 50, 0,None)
        self.set_search_area_design()
        
        self.ui.like_empty_notice.hide()
        
        self.like_icon_empty = SubWinUiManager(self.ui).like_icon_empty
        self.ui.like_btn.setIcon(self.like_icon_empty)

        # LikeState()
        self.like_active = False

        self.toggle_open =QPixmap("/nas/spirit/asset_project/source/toggle_open.png")
        self.toggle_like = QPixmap("/nas/spirit/asset_project/source/toggle_like.png")

        info_list_bar_s=QPixmap("/nas/spirit/asset_project/source/info_list_bar.png")
        self.ui.info_list_bar_s.setPixmap(info_list_bar_s)
    
        self.ui.toggle_btn.setPixmap(self.toggle_open) 
        bg =QPixmap("/nas/spirit/asset_project/source/bg.png")
        
        self.ui.label.setPixmap(bg)

        #사이드 바 기본 설정 
        self.ui.stackedWidget.hide()
    
        # 사이드 바 안에 이미지 롤링 배너 안 stackedwidget에 속한 위젯 지우기
        self.ui.stackedWidget_2.removeWidget(self.ui.page)
        self.ui.stackedWidget_2.removeWidget(self.ui.page_2)

        #정렬 콤보박스를 바꾸면 set_sorting_option 메서드로 연결
        
    def user_num(self):
        self.ui.user_num.setText("b976211")
