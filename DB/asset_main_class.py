from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy, QAbstractScrollArea
import sys

class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.user_num()
        self.table_widget()
        self.setup_tree()


    def setup_tree(self):
        """ 하나의 QTreeView에서 여러 카테고리를 관리하는 트리 설정 """
        self.ui.treeView.setStyleSheet(self.tree_style())
        model = QStandardItemModel()
        self.ui.treeView.setModel(model)
        self.ui.treeView.header().setVisible(False)  # 헤더 숨기기
        
        categories = {
            "Asset": ["3D Model", "Material", "HDRI", "Texture"],
            "Category": ["Character", "Environment", "Prop", "Vehicle", "Weapon", "Architecture", "Others"],
            "Style": ["Realistic", "Stylized", "Procedural"],
            "Resolution": ["512x512", "1024x1024", "2048x2048", "4096x4096"],
            "Polygon Count": ["Low-poly", "Mid-poly", "High-poly"]
        }
        
        for category, items in categories.items():
            parent_item = QStandardItem(category)
            parent_item.setCheckable(True)
            for item in items:
                child_item = QStandardItem(item)
                child_item.setCheckable(True)
                parent_item.appendRow(child_item)
            model.appendRow(parent_item)
        
        self.ui.treeView.expandAll()

    def setup_all_trees(self):
        self.setup_tree(self.ui.treeView, "Asset", ["3D Model", "Material", "HDRI", "Texture"])
        self.setup_tree(self.ui.treeView_2, "Category", ["Character", "Environment", "Prop", "Vehicle", "Weapon", "Architecture", "Others"])
        self.setup_tree(self.ui.treeView_3, "Style", ["Realistic", "Stylized", "Procedural"])
        self.setup_tree(self.ui.treeView_4, "Resolution", ["512x512", "1024x1024", "2048x2048", "4096x4096"])
        self.setup_tree(self.ui.treeView_5, "Polygon Count", ["Low-poly", "Mid-poly", "High-poly"])

    def tree_style(self):
        return """
        QTreeView::indicator {
            width: 8px;
            height: 8px;
            border-radius: 6px;  /* 반지름을 6px로 설정해서 원형으로 */
            border: 2px solid white;
            background-color: transparent;
        }
        
        QTreeView::indicator:checked {
            background-color: #ffffff;
            border-radius: 6px;
            border: 4px solid #6058EB;
        }
        
        QTreeView::indicator:unchecked {
            background-color: transparent;  /* 체크되지 않은 상태의 색상 */
            border: 2px solid #404040;
        }
        """


            

    def table_widget(self):
        assets = [
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_eldritch_metal_floor_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_perforated_eldritch_stone_wall_default.png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default (사본).png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default (또 다른 사본).png"},
            {"thumbnail": "/home/llly/spirit/source/asset_sum/thumbnail_abyssal_pipes_column_trim_default (3번째 사본).png"}
        ]



        self.ui.tableWidget.horizontalHeader().setVisible(False)  # 열(가로) 헤더 숨기기
        self.ui.tableWidget.verticalHeader().setVisible(False)  # 행(세로) 헤더 숨기기

        max_columns = 5  # 한 줄에 최대 5개 배치
        rows = (len(assets) + max_columns - 1) // max_columns  # 행 개수 계산

        self.ui.tableWidget.setRowCount(rows)  # 행 개수 설정
        self.ui.tableWidget.setColumnCount(max_columns)  # 열 개수 설정

        for index, asset in enumerate(assets):
            row_index = index // max_columns  # 행 번호 계산
            col_index = index % max_columns   # 열 번호 계산
            self.add_thumbnail(row_index, col_index, asset["thumbnail"])
        

    def add_thumbnail(self, row, col, thumbnail_path):
        """썸네일 이미지를 추가"""
        pixmap = QPixmap(thumbnail_path)
        if pixmap.isNull():
            print(f"❌ 이미지 로드 실패: {thumbnail_path}")
        pixmap = pixmap.scaled(160, 160)

        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        self.ui.tableWidget.setCellWidget(row, col, label)  # 행과 열에 이미지 추가

    def user_num(self):
        self.ui.user_num.setText("b976211")

    def load_ui(self):
        ui_file_path = "./asset_main2.ui"
        ui_file = QFile(ui_file_path)  
        loader = QUiLoader() 
        self.ui = loader.load(ui_file) 

        self.ui.show()  
        ui_file.close()

app = QApplication(sys.argv)
window = MainUi()
app.exec()
