import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QApplication
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer

class VideoWidget(QWidget):
    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(self.video_path)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Set to 30 ms for roughly 30 FPS

        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video if it ends
            return

        # Convert the frame to RGB (OpenCV uses BGR by default)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to QImage
        h, w, c = rgb_frame.shape
        qt_image = QImage(rgb_frame.data, w, h, 3 * w, QImage.Format_RGB888)

        # Set the QImage to QLabel
        self.label.setPixmap(QPixmap.fromImage(qt_image))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        video_path = "/nas/spirit/DB/thum/3d_assets/turnaround/3d_turnaround.mp4"
        
        self.stacked_widget = QStackedWidget(self)
        self.video_widget = VideoWidget(video_path)

        self.stacked_widget.addWidget(self.video_widget)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

        self.setWindowTitle("OpenCV Video Player with PySide6")
        self.show()

# Make sure to run the Qt Application loop
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
