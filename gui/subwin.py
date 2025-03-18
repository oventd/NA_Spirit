# 로거 파일 추가해서 유저가 중요한 
##### json 파일은 나스피릿에 넣고 이그노어 에 포함

try:
    from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QGraphicsOpacityEffect
    from PySide6.QtCore import QFile, Qt, Signal, QEvent, QObject, QUrl
    from PySide6.QtGui import QPixmap, QIcon
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QSizePolicy, QVBoxLayout
    from PySide6.QtMultimedia import QMediaPlayer
    from PySide6.QtMultimediaWidgets import QVideoWidget
except:
    from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QGraphicsOpacityEffect
    from PySide2.QtCore import QFile, Qt, Signal, QEvent, QObject, QUrl
    from PySide2.QtGui import QPixmap, QIcon
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QSizePolicy, QVBoxLayout
    from PySide2.QtMultimedia import QMediaPlayer
    from PySide2.QtMultimediaWidgets import QVideoWidget

from functools import partial
import sys
import os
import cv2


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
from constant import *
from video_player_manager import VideoPlayer

from like_state import LikeState

from asset import Asset
from gui.video_player_manager import VideoPlayer, VideoToImageExtractor


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

    def show_asset_detail_image(stackedWidget_2, detail_thum_urls, image_labels):
        detail_pixmap_urls = []  # 비디오에서 추출한 이미지를 저장할 리스트

        for img_path in detail_thum_urls:
            ext = os.path.splitext(img_path)[1]

            if ext == ".mp4":
                label = VideoPlayer(img_path)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(380, 291)  # 500x300 해상도로 고정
                stackedWidget_2.addWidget(label)

                # 비디오에서 프레임 추출
                image = VideoToImageExtractor(img_path)
                output_image_pixmap = image.save_frame()
                detail_pixmap_urls.append(output_image_pixmap)

                # 출력된 이미지 유효성 검사
                if output_image_pixmap.isNull():
                    print("Error: Failed to extract image from video.")
                else:
                    print("Image extracted successfully.")

                # detail_pixmap_urls에 저장된 이미지를 image_labels에 설정
                for idx, label in enumerate(image_labels):
                    if idx < len(detail_pixmap_urls):  # detail_pixmap_urls와 image_labels의 길이가 맞을 때
                        pixmap = detail_pixmap_urls[idx]
                        label.setPixmap(pixmap.scaled(80, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    else:
                        label.clear()

            elif ext == ".png":
                if img_path is None:
                    continue

                label = QLabel()
                pixmap = QPixmap(img_path)
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                stackedWidget_2.addWidget(label)

                # 썸네일을 이미지 레이블에 설정
                for idx, label in enumerate(image_labels):
                    if idx < len(detail_thum_urls) and detail_thum_urls[idx]:  # URL이 있는 경우에만 설정
                        pixmap = QPixmap(detail_thum_urls[idx])
                        label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    else:
                        label.clear()

        stackedWidget_2.setCurrentIndex(0)  # 0번째의 label을 보여준다.

 