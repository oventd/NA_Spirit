from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
import sys

class MultiVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # 🔹 창 설정
        self.setWindowTitle("Multi Video Player")  # 윈도우 제목 설정
        self.setGeometry(100, 100, 800, 600)  # 창 크기 설정

        # 🔹 여러 개의 `QMediaPlayer`, `QVideoWidget`을 저장할 리스트
        self.media_players = []  # 각 동영상 플레이어(QMediaPlayer) 리스트
        self.video_widgets = []  # 각 동영상을 표시할 `QVideoWidget` 리스트
        self.labels = []  # QLabel 리스트 (비디오 컨테이너 역할)

        # 🔹 UI 초기화
        

    def init_ui(self):
        layout = QVBoxLayout()  # 전체 레이아웃 설정

        # 🔹 `QStackedWidget`을 사용하여 여러 개의 비디오 위젯을 관리
        self.stacked_widget = QStackedWidget()  # 여러 개의 QLabel을 관리하는 위젯
        layout.addWidget(self.stacked_widget)  # 레이아웃에 추가

        # 🔹 재생 버튼 추가 (0번째 동영상 재생)
        self.play_button = QPushButton("▶ 재생 (0번 영상)")
        self.play_button.clicked.connect(lambda: self.play(0))  # 0번째 동영상 재생
        layout.addWidget(self.play_button)

        # 🔹 다음 동영상 재생 버튼 추가
        self.next_button = QPushButton("▶ 다음 영상")
        self.next_button.clicked.connect(self.next_video)  # 다음 동영상 재생
        layout.addWidget(self.next_button)

        self.setLayout(layout)  # 전체 레이아웃 설정

    def show_asset_detail_video(self, stacked_widget, video_urls):
        """
        여러 개의 동영상을 `QMediaPlayer`를 사용하여 관리하는 함수
        """
        self.stacked_widget = stacked_widget
        if not video_urls:
            print("❌ 동영상 목록이 비어 있습니다.")
            return

        # 🔹 기존 저장된 리스트 초기화
        self.media_players.clear()  # 기존 `QMediaPlayer` 리스트 초기화
        self.video_widgets.clear()  # 기존 `QVideoWidget` 리스트 초기화
        self.labels.clear()  # 기존 `QLabel` 리스트 초기화

        # 🔹 `QStackedWidget` 초기화 (기존 위젯 제거)
        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()  # 🔹 메모리에서 완전히 제거

        # 🔹 `for` 루프를 활용하여 여러 개의 비디오 생성
        for video_path in video_urls:
            if not video_path:
                continue  # 유효하지 않은 경로 건너뛰기

            # 🔹 QLabel 생성 (비디오 컨테이너 역할)
            widget = QWidget()
   
            # 🔹 QLabel 안에 `QVBoxLayout` 추가
            layout = QVBoxLayout(widget)


            # 🔹 개별적인 `QVideoWidget` 생성 (각 동영상마다 별도로 생성)
            video_widget = QVideoWidget()
            layout.addWidget(video_widget)  # 비디오 위젯을 QLabel 내부에 추가

            # 🔹 개별적인 `QMediaPlayer` 생성
            media_player = QMediaPlayer()
            media_player.setVideoOutput(video_widget)  # 해당 `QVideoWidget`에 연결
            media_player.setSource(QUrl.fromLocalFile(video_path))  # 동영상 경로 설정

            # 🔹 리스트에 저장 (객체 유지)
            self.media_players.append(media_player)  # `QMediaPlayer` 저장
            self.video_widgets.append(video_widget)  # `QVideoWidget` 저장
            self.labels.append(widget)  # `QLabel` 저장

            # 🔹 `QStackedWidget`에 QLabel(비디오 포함) 추가
            self.stacked_widget.addWidget(widget)

        print("✅ 모든 동영상 로드 완료!")

    def play(self, index=0):
        """ 🔹 지정된 인덱스의 동영상을 재생하는 함수 """
        if not self.media_players:
            print("❌ 재생할 동영상이 없습니다.")
            return

        if index >= len(self.media_players):
            print(f"❌ 잘못된 인덱스: {index}")
            return

        # 🔹 현재 재생 중인 동영상이 있다면 정지
        for player in self.media_players:
            player.stop()  # 모든 동영상 정지

        # 🔹 현재 보여줄 QLabel 설정 (`stackedWidget` 활용)
        self.stacked_widget.setCurrentIndex(index)  # 해당 비디오 표시

        print(f"🎬 {index} 번째 동영상 재생 시작")
        self.media_players[index].play()  # 🔹 해당 인덱스의 동영상 재생

    def next_video(self):
        """ 🔹 다음 동영상으로 전환하는 함수 """
        if not self.media_players:
            return

        current_index = self.stacked_widget.currentIndex()  # 현재 인덱스 가져오기
        next_index = (current_index + 1) % len(self.media_players)  # 다음 인덱스 계산

        self.play(next_index)  # 다음 동영상 재생

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MultiVideoPlayer()

    # 테스트용 동영상 목록 (여러 개의 동영상을 추가)
    video_list = [
        "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4",
        "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4",
        "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4"
    ]

    player.show_asset_detail_video(video_list)  # 동영상 추가
    player.show()

    # 🔹 첫 번째 동영상 자동 재생
    player.play(0)

    sys.exit(app.exec())
