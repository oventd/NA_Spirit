from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import sys

class CarouselWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt 수동 슬라이드 배너")
        self.setGeometry(100, 100, 800, 400)
       

        # ✅ 메인 위젯 및 레이아웃 설정
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)  

        # ✅ QStackedWidget 생성 (배너 역할)
        self.carousel = QStackedWidget()
        layout.addWidget(self.carousel)

        # ✅ QLabel을 사용하여 배너 추가
        self.images = ["/nas/spirit/asset_project/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png", "/nas/spirit/asset_project/source/asset_sum/thumbnail_eldritch_metal_floor_trim_default.png", "banner3.jpg"]
        self.image_labels = []

        for img_path in self.images:
            label = QLabel()
            label.setFixedSize(160,160)
            pixmap = QPixmap(img_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(True)  # ✅ 이미지 크기 자동 조정
            self.carousel.addWidget(label)
            self.image_labels.append(label)

        print(self.image_labels)

        # ✅ 이전/다음 버튼 추가
        self.prev_button = QPushButton("◀ 이전")
        self.next_button = QPushButton("다음 ▶")

        self.prev_button.clicked.connect(self.prev_slide)
        self.next_button.clicked.connect(self.next_slide)

        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)

        self.setCentralWidget(container)

    def next_slide(self):
        """다음 배너로 이동"""
        current_index = self.carousel.currentIndex()
        next_index = (current_index + 1) % len(self.image_labels)  # ✅ 순환 구조
        self.carousel.setCurrentIndex(next_index)

    def prev_slide(self):
        """이전 배너로 이동"""
        current_index = self.carousel.currentIndex()
        prev_index = (current_index - 1) % len(self.image_labels)  # ✅ 순환 구조
        self.carousel.setCurrentIndex(prev_index)


# ✅ 앱 실행
app = QApplication(sys.argv)
window = CarouselWidget()
window.show()
app.exec()
