import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget
from PySide6.QtUiTools import QUiLoader  # .ui 파일을 동적으로 로드하는 데 사용
from PySide6.QtCore import QFile, Signal

class Widget(QWidget):
    # 사용자 정의 시그널
    value_changed = Signal(str)  # 버튼 클릭 시 값을 전달하기 위한 시그널

    def __init__(self):
        super().__init__()

        # .ui 파일을 로드
        ui_file = QFile("/home/rapa/NA_Spirit/gui/popup.ui")  # UI 파일 경로를 지정 (현재 경로에서 widget.ui 파일을 찾음)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  # UI 로드
        ui_file.close()

        # # 버튼 클릭 시 시그널 발생
        # self.ui.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # 버튼 클릭 시 입력된 값을 MainWindow로 전달하는 시그널 발생
        value = self.ui.lineEdit.text()  # 입력된 텍스트 가져오기
        self.value_changed.emit(value)  # 시그널 발생

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        # 메인 윈도우에 표시할 레이아웃 및 위젯
        self.label = QLabel("No input yet", self)
        self.label.setGeometry(50, 50, 200, 40)

        self.open_widget_button = QPushButton("Open Widget", self)
        self.open_widget_button.setGeometry(50, 100, 200, 40)

        # 버튼 클릭 시 위젯을 띄우는 슬롯 연결
        self.open_widget_button.clicked.connect(self.show_widget)

    def show_widget(self):
        # QWidget 창을 열고 시그널을 받아서 처리
        self.widget = Widget()
        self.widget.value_changed.connect(self.update_label)  # 시그널을 메인 윈도우의 슬롯에 연결
        self.widget.show()

    def update_label(self, value):
        # QWidget에서 전달된 값으로 라벨 업데이트
        self.label.setText(f"Received value: {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())