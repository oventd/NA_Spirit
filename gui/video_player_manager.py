import sys
import vlc
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStackedWidget, QHBoxLayout
from PySide6.QtCore import Qt
import re


class VLCVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        # VLC 인스턴스 및 플레이어 생성
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # 비디오 출력용 QWidget
        self.container = QWidget(self)
        self.container.setFixedSize(380, 261)

        # # 버튼 (재생/일시정지/정지)
        # self.play_button = QPushButton("🎬 재생", self)
        # self.play_button.clicked.connect(self.play_video)

        # self.pause_button = QPushButton("⏸️ 일시정지", self)
        # self.pause_button.clicked.connect(self.pause_video)

        # self.stop_button = QPushButton("⏹️ 정지", self)
        # self.stop_button.clicked.connect(self.stop_video)

        # # 레이아웃 설정
        # self.layout = QVBoxLayout(self)
        # self.btn_layout = QHBoxLayout(self)
        # self.layout.addWidget(self.container)
        # self.btn_layout.addWidget(self.play_button)
        # self.btn_layout.addWidget(self.pause_button)
        # self.btn_layout.addWidget(self.stop_button)
        # self.layout.addLayout(self.btn_layout)
        # self.layout.setContentsMargins(0, 0, 0, 0)

        # VLC가 QWidget을 비디오 출력으로 사용하도록 설정
        # if sys.platform.startswith("linux"): 
        #     self.media_player.set_xwindow(self.container.winId())
        # elif sys.platform == "win32": 
        #     self.media_player.set_hwnd(self.container.winId())  # ✅ 수정됨
        # elif sys.platform == "darwin": 
        #     self.media_player.set_nsobject(int(self.container.winId()))  # ✅ 수정됨

    def set_video_source(self, file_path, ):
        """ 비디오 파일 경로를 설정하고 재생 """
        file_path = self.clean_path(file_path)  # VLC에서 사용할 경로    
        if file_path:
            print(f"🎥 파일 경로 설정됨: {file_path}")  # 디버깅용 출력
            media = self.instance.media_new(file_path)
            self.media_player.set_media(media)
            self.media_player.play()  # ✅ 자동 재생
            return self.container  # ✅ `self.container`가 아니라 `self`를 반환

    def play_video(self):
        """비디오 재생"""
        self.media_player.play()

    def pause_video(self):
        """비디오 일시정지"""
        self.media_player.pause()

    def stop_video(self):
        """비디오 정지"""
        self.media_player.stop()

    def clean_path(self,path):
        """파일 경로에서 보이지 않는 특수문자 및 공백 제거"""
        return re.sub(r"[^\x21-\x7E]", "", path).strip()  # ASCII 범위의 정상 문자만 유지

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VLCVideoPlayer()
    window.set_video_source("/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4")
    window.show()
    sys.exit(app.exec())