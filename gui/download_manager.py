import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget,QListWidgetItem
from PySide6.QtUiTools import QUiLoader  # .ui 파일을 동적으로 로드하는 데 사용
from PySide6.QtCore import QFile, Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from ui_loader import UILoader  

# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from constant import *
from logger import *
from like_state import LikeState
from asset import Asset
from assetmanager import AssetService



class DownloadManager:
    
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DownloadManager, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            super().__init__()
            self.exm_list = []
            self.exemples = []
            self.download_list_asset ={}
            self.like_state = LikeState()
        
            ui_loader = UILoader("/home/rapa/NA_Spirit/gui/asset_main2.ui")
            self.ui = ui_loader.load_ui()
            self.ui.show()
            
            self.ui.like_download_btn_area.clicked.connect(self.download_likged_assets_all)
            self.ref_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/reference_toggle.png")
            self.import_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/import_toggle.png")
            self.ui.download_format_label.setPixmap(self.ref_download_toggle_pixmap)

            

            self.add_list_widget()
            self.setDownloadFormat = False  #False가 레퍼런스
            
    
    
            self.logger = create_logger(UX_DOWNLOAD_LOGGER_NAME, UX_DOWNLOAD_LOGGER_DIR)
    
    def download_likged_assets_all(self):
        print("전체 다운로드 버튼이 눌렸어요")
        self.ui.download_touch_area.clicked.disconnect()
        
        self.ui.download_format_touch_area.clicked.connect(self.set_download_format_all)
        self.ui.download_touch_area.clicked.connect(self.download_all)
        self.ui.exit_btn_2.clicked.connect(self.exit_sub_bar_all)
        self.ui.cancel_touch_area.clicked.connect(self.exit_sub_bar_all)
        self.ui.download_listwidget.clear()
        
      
        self.exemples = self.like_state.like_asset_list
        self.download_list_asset=AssetService.get_assets_by_ids(self.exemples)
        self.add_list_widget()

        self.ui.stackedWidget.show()
        self.ui.stackedWidget.setCurrentIndex(2)

        self.logger.info(f"유저가 {self.exemples}를 다운받았어요")
   
    def download_assets_one(self):
        print("단일 에셋의 다운로드 버튼이 눌렸어요")
        self.ui.stackedWidget.setCurrentIndex(1)
        
        asset_one=asset = Asset().current

        print(f"다운로드하는 에셋 :{asset_one}")
       
       
        self.add_list_widget()
       

    def exit_sub_bar_all(self):
        self.ui.stackedWidget.hide()
        print("저 전으로 돌아갈 건데요")

    def exit_download_bar(self):
        self.ui.stackedWidget.setCurrentIndex(0)

        self.logger.info(f"유저가 단일 에셋을 다운받았어요")
    
    def set_download_format_all(self):
        if self.setDownloadFormat == False:
            self.setDownloadFormat = True #임포트
            self.ui.download_format_label.setPixmap(self.import_download_toggle_pixmap)
        else:
            self.setDownloadFormat = False
            self.ui.download_format_label.setPixmap(self.ref_download_toggle_pixmap)

    def add_list_widget(self):
        """동적으로 리스트 위젯의 항목을 추가하는 메서드"""

        for item_text in self.download_list_asset:
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
            



            
    def download_all(self):
        for i in range(self.ui.download_listwidget.count()):
            item = self.ui.download_listwidget.item(i)
            print(f"아이템: {item.text()}, 체크 상태: {item.checkState()}")
        download_fix_list=[self.ui.download_listwidget.item(i).text() for i in range(self.ui.download_listwidget.count()) if self.ui.download_listwidget.item(i).checkState() == Qt.Checked]
        selected_ids_list = [self.download_list_asset[name] for name in download_fix_list if name in self.download_list_asset]

        #다운로드 에셋에 다운로드 fix 리스트가 있다면 반환 및 리스트 벨류만 추가 


        if self.setDownloadFormat == False:
            print(f"{selected_ids_list}이 레퍼런스로 다운로드되었습니다")
        else:  
            print(f"{selected_ids_list}에셋이 임포트로 다운되었습니다")

    

    def on_button_click(self):
        # 버튼 클릭 시 입력된 값을 MainWindow로 전달하는 시그널 발생
        value = self.ui.lineEdit.text()  # 입력된 텍스트 가져오기