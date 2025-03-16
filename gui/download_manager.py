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
from check import Check
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
        
            ui_loader = UILoader("/home/llly/NA_Spirit/gui/asset_main2.ui")
            self.ui = ui_loader.load_ui()
            self.ui.show()
            
            self.ref_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/reference_toggle.png")
            self.import_download_toggle_pixmap = QPixmap("/nas/spirit/asset_project/source/popup_source/import_toggle.png")
            self.ui.download_format_label.setPixmap(self.ref_download_toggle_pixmap)

            

            self.add_list_widget()
            self.setDownloadFormat = False  #False가 레퍼런스
            self.ui.like_download_btn_area.clicked.connect(self.download_likged_assets_all)
            self.ui.download_format_touch_area.clicked.connect(self.set_download_format)
            self.ui.download_touch_area.clicked.connect(self.download)
            self.ui.exit_btn_2.clicked.connect(self.exit_download_bar)
            self.ui.cancel_touch_area.clicked.connect(self.exit_sub_bar)
    
    
            self.logger = create_logger(UX_DOWNLOAD_LOGGER_NAME, UX_DOWNLOAD_LOGGER_DIR)
    
    def download_likged_assets_all(self):
        print("전체 다운로드 버튼이 눌렸어요")
        
        filter_conditions = {}
        
        if Check().dict:
            
            filter_conditions[OBJECT_ID] = LikeState().like_asset_list
            
        assets  = list(AssetService.get_all_assets(filter_conditions=filter_conditions, sort_by=None, limit=0, skip=0,user_query = None)) # 모두 가져올거기 때문에 filter_conditions 는 빈딕셔너리
        self.ui.stackedWidget.show()
        self.ui.stackedWidget.setCurrentIndex(1)

        self.logger.info(f"유저가 관심에셋 전체를 다운받았어요")
   
    def download_assets_one(self):
        print("단일 에셋의 다운로드 버튼이 눌렸어요")
        self.ui.stackedWidget.setCurrentIndex(1)
        self.exemples = self.like_state.like_asset_list
        self.download_list_asset=AssetService.get_assets_by_ids(self.exemples)
        self.add_list_widget()
       

    def exit_sub_bar(self):
        self.ui.stackedWidget.hide()
        print("저 전으로 돌아갈 건데요")

    def exit_download_bar(self):
        self.ui.stackedWidget.setCurrentIndex(0)

        


        self.logger.info(f"유저가 단일 에셋을 다운받았어요")
    
    def set_download_format(self):
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
            



            
    def download(self):
        
        download_fix_list=self.get_checked_items(self.ui.download_listwidget)
        info=self.find_id(download_fix_list)
        print(info)
        if self.setDownloadFormat == False:
            print(f"{download_fix_list}이 레퍼런스로 다운로드되었습니다")
        else:  
            print(f"{download_fix_list}에셋이 임포트로 다운되었습니다")

    def find_id(self, download_list_name):
        download_dict = {}
        for name in download_list_name:
            for item in self.exemples:  # dict 대신 item 사용
                if name in item:  # 키 비교
                    id_value = item[name]  # 올바른 값 가져오기
                    download_dict[id_value] = name  # id를 키로 저장
        return download_dict  # 루프가 끝난 후 반환


    def get_checked_items(self, list_widget):
        return [list_widget.item(i).text() for i in range(list_widget.count()) if list_widget.item(i).checkState() == Qt.Checked]



    def on_button_click(self):
        # 버튼 클릭 시 입력된 값을 MainWindow로 전달하는 시그널 발생
        value = self.ui.lineEdit.text()  # 입력된 텍스트 가져오기