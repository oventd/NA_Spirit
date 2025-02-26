from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, Signal
import sys

class ClickableLabel(QLabel):
    clicked = Signal()  # PyQt의 pyqtSignal 대신 PySide6에서는 Signal 사용

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 클릭 이벤트 발생

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = ClickableLabel("클릭해보세요")
        self.label.clicked.connect(self.on_label_clicked)  # 클릭 시그널 연결

        layout.addWidget(self.label)
        self.setLayout(layout)

    def on_label_clicked(self):
        self.label.setText("라벨이 클릭되었습니다!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
