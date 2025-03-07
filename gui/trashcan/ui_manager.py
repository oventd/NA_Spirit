from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader

class UiManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = None

    def setup_ui(self):
        ui_file_path = "/home/rapa/NA_Spirit/gui/asset_main2.ui"
        ui_file = QFile(ui_file_path)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.main_window.ui = self.ui
        ui_file.close()
        
        self._setup_initial_settings()
    
    def _setup_initial_settings(self):
        """UI 초기 설정"""
        self.ui.stackedWidget.hide()
        self.ui.like_empty_notice.hide()
        
        self.ui.toggle_btn.setPixmap(QPixmap("/nas/spirit/asset_project/source/toggle_open.png"))
        self.ui.label.setPixmap(QPixmap("/nas/spirit/asset_project/source/bg.png"))
        
        self.ui.like_btn.setIcon(QIcon("/nas/spirit/asset_project/source/like_icon.png"))