#점심시간 테스트
import sys
import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QLabel

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        # 레이아웃과 위젯 설정
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # QLabel을 stackedWidget에 추가
        self.label = QLabel(self)
        self.stacked_widget.addWidget(self.label)

        # 비디오 캡처 객체 (동영상 파일 경로 설정)
        self.cap = cv2.VideoCapture('/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4')

        # 비디오가 열렸는지 확인
        if not self.cap.isOpened():
            print("Error: Unable to open video.")
            sys.exit()

        # 타이머 설정 (프레임 업데이트)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1000 / 30)  # 30fps로 업데이트

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            # BGR에서 RGB로 변환
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # QImage로 변환
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # QPixmap으로 변환하여 QLabel에 설정
            pixmap = QPixmap.fromImage(qimg)
            self.label.setPixmap(pixmap)

        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 동영상 끝나면 처음으로 돌아가기

    def closeEvent(self, event):
        self.cap.release()  # 비디오 캡처 객체 해제
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
