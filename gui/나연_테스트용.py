from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl
import sys

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # 창 설정
        self.setWindowTitle("PySide6 Video Player")
        self.setGeometry(100, 100, 800, 600)

        # 레이아웃 생성
        layout = QVBoxLayout()

        # 비디오 위젯 생성
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        # 오디오 출력 설정 (없으면 오류 발생 가능)
        self.audio_output = QAudioOutput()
        
        # 미디어 플레이어 생성
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)  # 오디오 출력 추가

        # 동영상 파일 설정
        video_path = "/nas/spirit/DB/thum/3d_assets/turnaround/turnaround.mp4"  # 로컬 파일 사용
        self.media_player.setSource(QUrl.fromLocalFile(video_path))

        # 재생 버튼 추가
        play_button = QPushButton("Play")
        play_button.clicked.connect(self.start_video)
        layout.addWidget(play_button)

        # 🔹 상태 변화 감지
        self.media_player.playbackStateChanged.connect(self.handle_state_change)

        self.setLayout(layout)

    def start_video(self):
        print("🎬 동영상 재생 시작")
        self.media_player.play()

    def handle_state_change(self, state):
        print(f"📢 현재 상태: {state}")
        if state == QMediaPlayer.PlaybackState.PlayingState:
            print("▶️ 재생 중")
        elif state == QMediaPlayer.PlaybackState.PausedState:
            print("⏸ 일시 정지 상태")
        elif state == QMediaPlayer.PlaybackState.StoppedState:
            print("⏹ 정지 상태")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
