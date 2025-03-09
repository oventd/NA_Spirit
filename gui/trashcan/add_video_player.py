from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
import sys

class MultiVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # 🔹 창 설정
        self.setWindowTitle("Multi Video Player")
        self.setGeometry(100, 100, 800, 600)

        # 🔹 여러 개의 `QMediaPlayer`, `QVideoWidget`을 저장할 리스트
        self.media_players = []
        self.video_widgets = []
        self.labels = []

        # 🔹 UI 초기화
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 🔹 `QStackedWidget`을 사용하여 여러 개의 비디오 위젯을 관리
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

        # 🔹 재생 및 다음 버튼을 별도의 독립된 버튼으로 생성
        self.play_button = QPushButton("▶ 재생 (0번 영상) [1]")
        self.play_button.setGeometry(50, 550, 120, 40)
        self.play_button.clicked.connect(lambda: self.play(0))
        self.play_button.setParent(self)  # 별도의 부모 위젯 설정

        self.next_button = QPushButton("▶ 다음 영상 [2]")
        self.next_button.setGeometry(200, 550, 120, 40)
        self.next_button.clicked.connect(self.next_video)
        self.next_button.setParent(self)

    def show_asset_detail_video(self,stacked_widget, video_urls):
        if not video_urls:
            print("❌ 동영상 목록이 비어 있습니다.")
            return
        self.stacked_widget=stacked_widget
        self.media_players.clear()
        self.video_widgets.clear()
        self.labels.clear()

        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

        for video_path in video_urls:
            if not video_path:
                continue

            widget = QWidget()
            layout = QVBoxLayout(widget)

            video_widget = QVideoWidget()
            layout.addWidget(video_widget)

            media_player = QMediaPlayer()
            media_player.setVideoOutput(video_widget)
            media_player.setSource(QUrl.fromLocalFile(video_path))

            self.media_players.append(media_player)
            self.video_widgets.append(video_widget)
            self.labels.append(widget)

            self.stacked_widget.addWidget(widget)

        print("✅ 모든 동영상 로드 완료!")

    def play(self, index=0):
        if not self.media_players:
            print("❌ 재생할 동영상이 없습니다.")
            return

        if index >= len(self.media_players):
            print(f"❌ 잘못된 인덱스: {index}")
            return

        for player in self.media_players:
            player.stop()

        self.stacked_widget.setCurrentIndex(index)

        print(f"🎬 {index} 번째 동영상 재생 시작")
        self.media_players[index].play()

    def next_video(self):
        if not self.media_players:
            return

        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % len(self.media_players)

        self.play(next_index)

