try:
    from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget,QGraphicsOpacityEffect
except:
    from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QGraphicsOpacityEffect

import sys
import os

current_file_path = os.path.abspath(__file__)
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:
        sys.path.append(root)

from constant import *
from assetmanager import AssetManager
from default_ui_manager import DefaultUiManager
from table_ui_manager import TableUiManager
from tree_ui_manager import TreeUiManager
from ui_loader import UILoader  

class MainUi(QMainWindow):
    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MainUi, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """초기 화면에 필요한 클래스를 호출하고 객체에 저장 """
        if not hasattr(self, "_initialized"):  
            super().__init__()
            ui_loader = UILoader("/home/llly/NA_Spirit/gui/asset_main2.ui")
            self.ui = ui_loader.load_ui()
            self.ui.show()
            AssetManager() #에셋 
            TableUiManager()
            DefaultUiManager()
            TreeUiManager()
            self._initialized = True  
        else:
            self.ui.show()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUi()
    app.exec()


#메인 앱 정리 완료
#assetmanager/ table 정리중