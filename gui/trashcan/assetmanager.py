from asset_service import AssetService
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

class AssetManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        
    def load_assets(self, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        """자산 데이터를 테이블에 로드"""
        assets = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip))
        self.display_assets(assets)
    
    def display_assets(self, assets):
        """자산을 UI 테이블에 표시"""
        max_columns = 5
        rows = (len(assets) // max_columns) + 1
        self.ui.tableWidget.setRowCount(rows)
        self.ui.tableWidget.setColumnCount(max_columns)
        
        for index, asset in enumerate(assets):
            row_index = index // max_columns
            col_index = index % max_columns
            self.add_thumbnail(row_index, col_index, asset)
    
    def add_thumbnail(self, row, col, asset):
        """자산 썸네일을 테이블에 추가"""
        thumbnail_path = asset["preview_url"]
        asset_name = asset["name"]
        asset_type = asset["asset_type"]
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setAlignment(Qt.AlignTop)
        
        thumbnail_label = QLabel()
        name_label = QLabel(asset_name)
        type_label = QLabel(asset_type)
        
        pixmap = QPixmap(thumbnail_path)
        thumbnail_label.setPixmap(pixmap)
        thumbnail_label.setFixedHeight(160)
        thumbnail_label.setAlignment(Qt.AlignCenter)
        
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        name_label.setFixedHeight(14)
        
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        type_label.setFixedHeight(18)
        
        layout.addWidget(thumbnail_label)
        layout.addWidget(name_label)
        layout.addWidget(type_label)
        widget.setLayout(layout)
        
        self.ui.tableWidget.setCellWidget(row, col, widget)
        self.ui.tableWidget.resizeRowsToContents()
