from PySide6.QtWidgets import QListWidgetItem, QPushButton, QVBoxLayout, QWidget, QListWidget, QApplication
from PySide6.QtCore import Qt, QFile
from PySide6.QtUiTools import QUiLoader
# import sys
# sys.path.append('/home/rapa/NA_Spirit/upload')
# from get_sgtk_info import ShotGridAssetManager

class ShotGridAssetUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        loader=QUiLoader()
        self.ui=loader.load("/home/rapa/NA_Spirit/upload/gui/ui/shotgrid.ui")
        self.ui.show()
        
        self.ui.remove_button.clicked.connect(self.download_all)
        self.ui.assetname_listwidget.itemChanged.connect(self.update_item_state)

        # self.asset_manager = ShotGridAssetManager()

    
    def add_list_widget(self,asset):
        """동적으로 리스트 위젯의 항목을 추가하는 메서드"""
        for item_text in asset:
            item = QListWidgetItem(item_text)  # 항목 생성
            item.setCheckState(Qt.Checked)  # 체크박스를 체크된 상태로 설정
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
        return download_fix_list
    
    def update_item_state(self, item):
        """체크박스 상태 변경 시 실시간으로 반영"""
        if item.checkState() == Qt.Checked:
            print(f"{item.text()} 항목이 체크되었습니다.")
        else:
            print(f"{item.text()} 항목이 체크 해제되었습니다.")
    
# PySide6 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication()
    window = ShotGridAssetUI()
    window.add_list_widget(["Asset 1", "Asset 2", "Asset 3"])
    app.exec()