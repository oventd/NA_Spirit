import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget,QListWidgetItem
from PySide6.QtUiTools import QUiLoader  # .ui 파일을 동적으로 로드하는 데 사용
from PySide6.QtCore import QFile, Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap



class Widget(QWidget):
    # 사용자 정의 시s그널
    value_changed = Signal(str)  # 버튼 클릭 시 값을 전달하기 위한 시그널

    def __init__(self):
        super().__init__()
        self.exemple = ["apple", "banana", "cherry","cherry","cherry","cherry","cherry","cherry","cherry","cherry","cherry"]
        self.load_ui()
        self.add_list_widget()
        self.setWindowTitle("Download Popup")  # 윈도우 제목
        self.setWindowFlags(Qt.FramelessWindowHint)  # 외곽선과 헤더를 없앰
        self.ui.cancel_touch_area.clicked.connect(self.close)
        self.ref_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/reference_toggle.png")
        self.import_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/import_toggle.png")

        self.setDownloadFormat = False  #False가 레퍼런스
        self.ui.download_format_touch_area.clicked.connect(self.set_download_format)
        self.ui.download_touch_area.clicked.connect(self.download)

        

    def load_ui(self):
        # .ui 파일을 로드
        ui_file = QFile("/home/llly/NA_Spirit/gui/popup.ui")  # UI 파일 경로를 지정 (현재 경로에서 widget.ui 파일을 찾음)
        loader = QUiLoader()
        self.ui = loader.load(ui_file, self)  # UI 로드
        ui_file.close()
        
    def set_download_format(self):
        if self.setDownloadFormat == False:
            self.setDownloadFormat = True #임포트
            self.ui.download_format_label.setPixmap(self.import_download_toggle_pixmap)
        else:
            self.setDownloadFormat = False
            self.ui.download_format_label.setPixmap(self.ref_download_toggle_pixmap)

    def add_list_widget(self):
        for item_text in self.exemple:
            item = QListWidgetItem(item_text)  # 항목 생성
            item.setCheckState(Qt.Unchecked)  # 체크박스를 체크된 상태로 설정
            self.ui.download_listwidget.addItem(item) 
        self.list_widget_stylesheet()

    def list_widget_stylesheet(self):

        self.ui.download_listwidget.setStyleSheet("""
            QListWidget {
                background-color: #101011;  /* 리스트의 배경을 투명하게 설정 */
                color:#ffffff;
            }

            QListWidget::item:checked::indicator {
            
                border-radius: 50%;  /* 체크박스를 원형으로 설정 */
                width: 16px;  /* 체크박스 크기 설정 */
                height: 24px;
            }

            QListWidget::item:unchecked::indicator {
             
                border: 0.5px solid #ffffff;  /* 체크박스의 테두리 색상 */
                border-radius: 50%;  /* 체크박스를 원형으로 설정 */
                width: 16px;  /* 체크박스 크기 설정 */
                height: 24px;
            }
        """)
            
            
    def download(self):
        if self.setDownloadFormat == False:
            print("apple에셋이 레퍼런스로 다운로드되었습니다")
        else:  
            print("apple에셋이 임포트로 다운되었습니다")

    

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