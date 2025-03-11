from PySide6.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

class DynamicCircleLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Pretendard", 8, QFont.Weight.Medium))  # 글꼴 설정
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 텍스트 중앙 정렬
        self.setStyleSheet("""
            background-color: #6E3AEF;
            color: white;
            border-radius: 7.5px;

        """)  
        self.update_size()

    def update_size(self):
        """ 텍스트 길이에 따라 QLabel 크기 조정 """
        text_width = self.fontMetrics().horizontalAdvance(self.text())  # 텍스트 너비 계산
        self.setFixedWidth(max(11, text_width + 11))  # 최소 40px 유지, 텍스트 크기에 맞게 확장
        self.setFixedHeight(16)  # 높이는 고정

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    # 예제 라벨 3개
    label1 = DynamicCircleLabel("1")
    label2 = DynamicCircleLabel("123")
    label3 = DynamicCircleLabel("1234567")

    layout.addWidget(label1)
    layout.addWidget(label2)
    layout.addWidget(label3)
    
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
