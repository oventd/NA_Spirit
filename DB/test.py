


from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
import sys

class ClickableLabel(QLabel):
    """클릭 가능한 QLabel"""
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        """QLabel 클릭 시 신호 발생"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QStackedWidget + QLabel 슬라이드 (좌우 버튼 포함)")
        self.setGeometry(100, 100, 800, 400)

        # ✅ UI 구성
        container = QWidget()
        main_layout = QVBoxLayout()  # 메인 레이아웃
        container.setLayout(main_layout)

        # ✅ QStackedWidget 생성
        self.stackedWidget = QStackedWidget()
        main_layout.addWidget(self.stackedWidget)

        # ✅ 이미지 리스트
        self.images = ["/nas/spirit/DB/thum/grill_presetting_001.png", "/nas/spirit/DB/thum/grill_presetting_002", "/nas/spirit/DB/thum/grill_presetting_001.png"]

        # ✅ QLabel을 QStackedWidget에 추가
        for img_path in self.images:
            label = ClickableLabel(self)
            pixmap = QPixmap(img_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setScaledContents(True)

            self.stackedWidget.addWidget(label)

        self.stackedWidget.setCurrentIndex(0)  # ✅ 첫 번째 배너로 시작

        # ✅ 좌우 버튼 추가 (레이아웃 포함)
        button_layout = QHBoxLayout()  # 좌우 정렬을 위한 레이아웃

        self.prev_button = QPushButton("◀ 이전")
        self.next_button = QPushButton("다음 ▶")

        self.prev_button.clicked.connect(self.prev_slide)
        self.next_button.clicked.connect(self.next_slide)

        button_layout.addWidget(self.prev_button)
        button_layout.addStretch()  # 버튼 사이 간격 조절
        button_layout.addWidget(self.next_button)

        main_layout.addLayout(button_layout)

        self.setCentralWidget(container)

    def next_slide(self):
        """다음 슬라이드 이동"""
        current_index = self.stackedWidget.currentIndex()
        next_index = (current_index + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(next_index)
        print("다음 이미지로 변경됨")

    def prev_slide(self):
        """이전 슬라이드 이동"""
        current_index = self.stackedWidget.currentIndex()
        prev_index = (current_index - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(prev_index)
        print("이전 이미지로 변경됨")

# ✅ 앱 실행
app = QApplication(sys.argv)
window = MainUi()
window.show()
app.exec()
