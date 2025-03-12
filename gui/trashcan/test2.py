import sys
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QPixmap, QImage
import cv2
from functools import partial

class SubWin:
    @staticmethod
    def show_asset_detail_image(stackedWidget_2, detail_thum_urls, image_labels):
        """Test method for showing asset detail images (both images and videos)"""
        # Simulate adding a video path
        video_path = "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4"
        detail_thum_urls.append(video_path)

        for img_path in detail_thum_urls:
            ext = os.path.splitext(img_path)[1]
            if ext == ".mp4":
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                stackedWidget_2.addWidget(label)
                
                # 영상의 크기를 QLabel에 맞게 설정
                label.setFixedSize(640, 480)  # 적당한 크기로 설정 (640x480)

                # 비디오를 위한 타이머와 프레임 업데이트 연결
                video_capture = cv2.VideoCapture(video_path)
                if not video_capture.isOpened():
                    print(f"Error: 비디오 파일을 열 수 없습니다. 경로를 확인해주세요: {video_path}")
                    return
                
                print(f"비디오 파일 열림: {video_path}")  # 비디오 파일이 열렸는지 확인하는 로그

                # Timer for frame updates
                video_player = SubWin.VideoPlayer(video_capture, label)
                timer = QTimer()
                timer.timeout.connect(video_player.update_frame)
                timer.start(30)  # 30ms마다 프레임을 업데이트 (약 30FPS)
            elif ext == ".png":
                if img_path is None:
                    continue
                label = QLabel()
                pixmap = QPixmap(img_path)
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                stackedWidget_2.addWidget(label)

        for idx, label in enumerate(image_labels):
            if idx < len(detail_thum_urls) and detail_thum_urls[idx]:  # If URL exists, update label
                pixmap = QPixmap(detail_thum_urls[idx])
                label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                label.clear()

        stackedWidget_2.setCurrentIndex(0)  # Show the first label
        print("Thumbnail images: " + str(detail_thum_urls))
        print("Image labels: " + str(image_labels))

    class VideoPlayer:
        def __init__(self, video_capture, label):
            self.video_capture = video_capture
            self.label = label

        def update_frame(self):
            """Update video frames in the QLabel"""
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: 비디오 프레임을 읽을 수 없습니다.")  # 프레임 읽을 수 없을 때 로그
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video if it ends
                return

            # 프레임이 제대로 읽혔는지 확인
            print(f"프레임 크기: {frame.shape}")

            # OpenCV는 BGR 형식으로 이미지를 읽기 때문에 RGB로 변환
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = rgb_frame.shape
            qt_image = QImage(rgb_frame.data, w, h, 3 * w, QImage.Format_RGB888)

            # QLabel에 QImage를 표시
            self.label.setPixmap(QPixmap.fromImage(qt_image))

    @staticmethod
    def next_slide(stackedWidget_2):
        """Move to the next slide"""
        current_index = stackedWidget_2.currentIndex()
        next_index = (current_index + 1) % stackedWidget_2.count()  # Wrap around
        stackedWidget_2.setCurrentIndex(next_index)
        print(f"Moved to next index: {next_index}")


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Asset Detail Image with Next Button")
        self.setGeometry(100, 100, 800, 600)

        # Create the stacked widget and image labels
        self.stackedWidget_2 = QStackedWidget(self)
        self.image_labels = [QLabel(self) for _ in range(4)]  # Create 4 labels for testing thumbnails

        # Create a layout and add the stacked widget and button
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget_2)

        # Create "Next" button
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(partial(SubWin.next_slide, self.stackedWidget_2))  # Connect to next_slide method
        layout.addWidget(self.next_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Dummy test data for images and videos
        detail_thum_urls = [
            "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4",  # 비디오 경로
            "/nas/spirit/DB/thum/texture/metal_presetting_001.png",   # 이미지 경로
            "/nas/spirit/DB/thum/texture/grill_presetting_002.png"   # 또 다른 이미지 경로
        ]

        # Call show_asset_detail_image with test data
        SubWin.show_asset_detail_image(self.stackedWidget_2, detail_thum_urls, self.image_labels)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
