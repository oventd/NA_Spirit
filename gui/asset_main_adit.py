
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
import os,sys
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from PySide6.QtWidgets import QApplication, QMainWindow
from ui_manager import *
from assetmanager import AssetManager
from eventhandler import EventHandler
import sys


class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        
        # UI 매니저 생성
        self.ui_manager = UiManager(self)
        self.event_handler = EventHandler(self)
        
        # UI 설정 및 이벤트 연결
        self.ui_manager.setup_ui()
        self.event_handler.connect_events()
        
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUi()
    app.exec()