from PySide6.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

class DynamicCircleLabel(QLabel):
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Pretendard", 6, QFont.Weight.Light))  # 글꼴 설정
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 텍스트 중앙 정렬
        self.setStyleSheet("""
            background-color: #6E3AEF;
            color: white;
            border-radius: 5px;

        """)  
        self.update_size()

    def update_size(self):
        """ 텍스트 길이에 따라 QLabel 크기 조정 """
        text_width = self.fontMetrics().horizontalAdvance(self.text())  # 텍스트 너비 계산
        self.setFixedWidth(max(8, text_width + 8))  # 최소 40px 유지, 텍스트 크기에 맞게 확장
        self.setFixedHeight(11)  # 높이는 고정
