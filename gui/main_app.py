# 로거 파일 추가해서 유저가 중요한
##### json 파일은 나스피릿에 넣고 이그노어 에 포함
#동영상 추가

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
import cv2
# from #점심시간테스트 import VLCVideoPlayer

# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from assetmanager import ClickableLabel

from constant import *


from trashcan.asset_manager import AssetManager
# from data_manager import DataManager
from default_ui_manager import DefaultUiManager

from table_ui_manager import TableUiManager
from tree_ui_manager import TreeUiManager

from assetmanager import AssetService
from download_manager import DownloadManager    


class MainUi(QMainWindow):
    _instance = None  # 싱글톤 인스턴스 저장

    clicked = Signal()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MainUi, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            super().__init__()

            self.load_ui()
            
            self.media_players = []  # 각 동영상 플레이어(QMediaPlayer) 리스트
            self.video_widgets = []  # 각 동영상을 표시할 `QVideoWidget` 리스트
            self.labels = []
            #"file_format", "updated_at", "downloads" << 가지고 있는 정렬 기준

            self.asset_manager = AssetManager(self.ui)
            self.table_ui_manager = TableUiManager(self.ui)
            self.default_ui_manager = DefaultUiManager(self.ui )

            self.tree_ui_manager = TreeUiManager(self.ui)
            self.download_manager = DownloadManager(self.ui)
            
            

            self._initialized = True  # 인스턴스가 초기화되었음을 표시
            

    def load_ui(self):
        ui_file_path = "/home/rapa/NA_Spirit/gui/asset_main2.ui"
        ui_file = QFile(ui_file_path)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)

        self.ui.show()
        ui_file.close()

app = QApplication(sys.argv)
window = MainUi()
app.exec()
