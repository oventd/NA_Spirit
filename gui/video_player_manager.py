import sys
import vlc
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

class VLCVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # VLC 인스턴스 및 플레이어 생성
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.setFixedSize(300, 300)  # 크기 설정

        # 비디오 출력용 QWidget
        self.container = QWidget(self)
        self.container.setFixedSize(300, 250)

        # 버튼 (재생/일시정지/정지)
        self.play_button = QPushButton("🎬 재생", self)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("⏸️ 일시정지", self)
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton("⏹️ 정지", self)
        self.stop_button.clicked.connect(self.stop_video)

        # 레이아웃 설정
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.container)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # VLC가 QWidget을 비디오 출력으로 사용하도록 설정
        if sys.platform.startswith("linux"): 
            self.media_player.set_xwindow(self.container.winId())
        elif sys.platform == "win32": 
            self.media_player.set_hwnd(self.container.winId())  # ✅ 수정됨
        elif sys.platform == "darwin": 
            self.media_player.set_nsobject(int(self.container.winId()))  # ✅ 수정됨

    def set_video_source(self, file_path):
        """ 비디오 파일 경로를 설정하고 재생 """
        if file_path:
            print(f"🎥 파일 경로 설정됨: {file_path}")  # 디버깅용 출력
            media = self.instance.media_new(file_path)
            self.media_player.set_media(media)
            self.media_player.play()  # ✅ 자동 재생
            return self  # ✅ `self.container`가 아니라 `self`를 반환

    def play_video(self):
        """비디오 재생"""
        self.media_player.play()

    def pause_video(self):
        """비디오 일시정지"""
        self.media_player.pause()

    def stop_video(self):
        """비디오 정지"""
        self.media_player.stop()