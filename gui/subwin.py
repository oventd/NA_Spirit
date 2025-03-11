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
import vlc

# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)


from assetmanager import AssetService  # AssetService 임포트
from assetmanager import ClickableLabel

from PySide6.QtCore import QObject, QEvent, Qt
from constant import *
from add_video_player import *
from video_player_manager import VLCVideoPlayer

from like_state import LikeState

from asset import Asset


class SubWin:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
    def __init__(self):
        pass
 
    @staticmethod 
    def next_slide(stackedWidget_2):
        """다음 슬라이드 이동"""
        current_index = stackedWidget_2.currentIndex()
        next_index = (current_index + 1) % stackedWidget_2.count()
        stackedWidget_2.setCurrentIndex(next_index)
        print(f"{next_index}다음 이미지로 변경됨")
    @staticmethod
    def prev_slide( stackedWidget_2):
        """이전 슬라이드 이동"""
        current_index = stackedWidget_2.currentIndex()
        prev_index = (current_index - 1) % stackedWidget_2.count()
        stackedWidget_2.setCurrentIndex(prev_index)
        print("이전 이미지로 변경됨")
      # 리뷰 순서를 정리를 

    def show_asset_detail_image(stackedWidget_2, detail_thum_urls , image_labels):

        for img_path in detail_thum_urls:
            if img_path == None:
                continue
            label = QLabel()
            pixmap = QPixmap(img_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            stackedWidget_2.addWidget(label)

        for idx, label in enumerate(image_labels):
            if idx < len(detail_thum_urls) and detail_thum_urls[idx]:  # URL이 있는 경우에만 설정
                pixmap = QPixmap(detail_thum_urls[idx])
                label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                label.clear()
        
        stackedWidget_2.setCurrentIndex(0)  # 0번째의 label을 보여준다. 
        print("디테일 썸네일 이미지 리스트>>>> " + str(detail_thum_urls))
        print("이미지라벨 4개 >>>>"+str(image_labels))
    
    @staticmethod

    def show_asset_detail_video(stackedWidget_2, turnaround_urls):
        """QStackedWidget에 VLC 기반 동영상 플레이어 추가"""

        for video_path in turnaround_urls:
            if video_path is None:
                continue  # 빈 값은 무시

            # ✅ VLC 비디오 플레이어 위젯 생성
            video_player = VLCVideoPlayer()
            video_widget = video_player.set_video_source(video_path)

            # ✅ QStackedWidget에 추가
            stackedWidget_2.addWidget(video_widget)

        stackedWidget_2.setCurrentIndex(0)  # 첫 번째 동영상을 표시
        stackedWidget_2.raise_()  # ✅ `stackedWidget_2`를 UI의 가장 앞(front)으로 이동

