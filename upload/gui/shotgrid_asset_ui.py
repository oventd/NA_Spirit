from PySide6.QtWidgets import QListWidgetItem, QPushButton, QVBoxLayout, QWidget, QListWidget, QApplication
from PySide6.QtCore import Qt, QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
import sgtk
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/upload')
from asset_upload_manager import AssetUploadManager

class ShotGridAssetUI(QWidget):
    # _instance = None  

    # def __new__(cls, *args, **kwargs):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def __init__(self, parent=None):
        if not hasattr(self, "_initialized"):
            super().__init__(parent)

            self.engine = sgtk.platform.current_engine()  # ShotGrid Toolkit 엔진 가져오기
            self.context = self.engine.context  # 컨텍스트 가져오기
            self.project_dir = self.get_project_directory()
            
            loader=QUiLoader()

            self.ui=loader.load("/home/rapa/NA_Spirit/upload/gui/ui/shotgrid.ui")
            self.ui.show()
            self.ui.setStatusBar(None)
            label_pixmap=QPixmap("/nas/spirit/asset_project/source/btn.png")
            self.ui.download_btn_one.setPixmap(label_pixmap)
            self.ui.remove_button.clicked.connect(self.download_all)
            self.ui.assetname_listwidget.itemChanged.connect(self.update_item_state)

            # self.asset_manager = ShotGridAssetManager()
            asset_paths = self.find_asset_paths()
            asset_names = []
            for asset_path in asset_paths:
                asset_name = os.path.basename(asset_path)
                asset_names.append(asset_name)

            self.add_list_widget(asset_names)

            self._initialized = True
        else:
            self.ui.show()        
    
    def add_list_widget(self,asset):
        """동적으로 리스트 위젯의 항목을 추가하는 메서드"""
        for item_text in asset:
            item = QListWidgetItem(item_text)  # 항목 생성
            item.setCheckState(Qt.Unchecked)  # 체크박스를 체크된 상태로 설정
            self.ui.assetname_listwidget.addItem(item) 
        self.list_widget_stylesheet()

    def list_widget_stylesheet(self):

        self.ui.assetname_listwidget.setStyleSheet("""
            QListWidget {
                background-color: #222222;  /* 리스트의 배경을 어두운 색으로 설정 */
                color: white;  /* 기본 텍스트 색상 흰색으로 설정 */
            }

            QListWidget::item {
                background-color: #222222;  /* 항목 배경색 어두운 색 */
                color: white;  /* 기본 항목 텍스트 색상 흰색 */
            }

            QListWidget::item:selected {
                color: white;  /* 선택된 항목 텍스트 색상 흰색 */
                background-color: #444444;  /* 선택된 항목 배경을 밝은 회색으로 설정 */
            }

            QListWidget::item:checked {
                color: black;  /* 체크된 항목의 텍스트 색상 검정색으로 설정 */
                background-color: #444444;  /* 체크된 항목 배경을 밝은 회색으로 설정 */
            }

            QListWidget::item:unchecked {
                color: white;  /* 체크되지 않은 항목 텍스트 색상 흰색으로 설정 */
                background-color: #222222;  /* 체크되지 않은 항목 배경을 어두운 색으로 설정 */
            }

            QListWidget::item:checked::indicator {
                border-radius: 50%;  /* 체크박스를 원형으로 설정 */
                width: 16px;  /* 체크박스 크기 설정 */
                height: 16px;  /* 체크박스 크기 설정 */
            }

            QListWidget::item:unchecked::indicator {
                border-radius: 50%;  /* 체크박스를 원형으로 설정 */
                width: 16px;  /* 체크박스 크기 설정 */
                height: 16px;  /* 체크박스 크기 설정 */                                
            }
        """)
    def get_project_directory(self) -> str:
        """
        현재 ShotGrid Toolkit 프로젝트의 루트 디렉토리를 반환.

        :return: 프로젝트 디렉토리 경로 (str)
        """
        if not self.context or not self.context.project:
            raise ValueError("현재 ShotGrid 프로젝트 컨텍스트를 찾을 수 없습니다.")

        # 프로젝트의 루트 디렉토리 가져오기
        tk = self.engine.sgtk
        return tk.project_path
    
    def get_checked_assets(self):
        """체크된 에셋 리스트를 반환"""
        checked_assets = []
        for i in range(self.ui.assetname_listwidget.count()):
            item = self.ui.assetname_listwidget.item(i)
            if item.checkState() == Qt.Checked:
                checked_assets.append(item.text())
                print(item.text())
        print(f"체크된 아이템 리스트: {checked_assets}")
        return checked_assets

    def download_all(self):
        """
        체크된 아이템을 기준으로 다운로드 또는 임포트 수행
        """
        print("버튼 눌림")
        # 체크된 아이템 리스트 추출
        download_fix_list = []
        for i in range(self.ui.assetname_listwidget.count()):
            item = self.ui.assetname_listwidget.item(i)
            if item.checkState() == Qt.Checked:
                download_fix_list.append(item.text())
        print(f"다운로드 픽스 리스트: {download_fix_list}")
        self.upload_assets(download_fix_list)
        return download_fix_list
    
    def upload_assets(self, download_fix_list):
        manager = AssetUploadManager()
        for asset_name in download_fix_list:
            manager.process_asset(asset_name)

    def update_item_state(self, item):
        """체크박스 상태 변경 시 실시간으로 반영"""
        if item.checkState() == Qt.Checked:
            print(f"{item.text()} 항목이 체크되었습니다.")
        else:
            print(f"{item.text()} 항목이 체크 해제되었습니다.")


    def find_asset_paths(self) -> list:
        """
        프로젝트 디렉토리의 assets 폴더에서 depth 1과 depth 2의 하위 폴더들을 리스트로 반환.

        :return: depth 1과 depth 2 하위 폴더들의 전체 경로 리스트
        """
        assets_directory = os.path.join(self.project_dir, "assets")

        if not os.path.exists(assets_directory):
            raise FileNotFoundError(f"경로가 존재하지 않습니다: {assets_directory}")

        # 1depth와 2depth 하위 폴더들을 리스트로 담기
        subfolder_paths = []

        for folder in os.listdir(assets_directory):
            folder_path = os.path.join(assets_directory, folder)

            if os.path.isdir(folder_path):
                # 2depth 하위 폴더들
                for subfolder in os.listdir(folder_path):
                    subfolder_path = os.path.join(folder_path, subfolder)
                    if os.path.isdir(subfolder_path):
                        subfolder_paths.append(subfolder_path)

        return subfolder_paths  # depth 1과 2 하위 폴더들의 경로 리스트 반환
# PySide6 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication()
    window = ShotGridAssetUI()
    window.add_list_widget(["Asset 1", "Asset 2", "Asset 3"])
    app.exec()