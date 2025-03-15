from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget

class UILoader:
    _instance = None

    def __new__(cls, ui_file_path):
        if not cls._instance:
            cls._instance = super(UILoader, cls).__new__(cls)
            cls._instance._init_ui(ui_file_path)
        return cls._instance

    def _init_ui(self, ui_file_path):
        self.ui_file_path = ui_file_path
        self.ui = None

    def load_ui(self) -> QWidget:
        if self.ui is None:
            ui_file = QFile(self.ui_file_path)
            loader = QUiLoader()
            self.ui = loader.load(ui_file)
            ui_file.close()
        return self.ui
