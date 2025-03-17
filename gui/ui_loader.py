from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget


class UILoader:
    _instance = None

    def __new__(cls, ui_file_path):
        if not cls._instance:
            cls._instance = super(UILoader, cls).__new__(cls)
        return cls._instance

    def __init__(self, ui_file_path):
        if hasattr(self, "_initialized"):  # 중복 초기화 방지
            return
        self._initialized = True  # 초기화 완료 여부 체크

        self.ui_file_path = ui_file_path
        self.ui = None

    def load_ui(self) -> QWidget:
        """ UI 파일을 로드하고 QWidget 객체를 반환 """
        if self.ui is None:
            ui_file = QFile(self.ui_file_path)
            loader = QUiLoader()
            self.ui = loader.load(ui_file)
            ui_file.close()
            self.ui.setStatusBar(None)
            self.ui.setFixedSize(1240, 799)
        return self.ui
