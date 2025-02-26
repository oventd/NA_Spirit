from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QTreeWidgetItem, QPushButton, QStyledItemDelegate
from PySide6.QtCore import QFile, Qt,QRect
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QPixmap,  QPainter, QBrush, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy, QAbstractScrollArea,QVBoxLayout
from functools import partial

import sys


class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.tree_widget()
        self.main_ui_setting()
        self.user_num()
        self.ui.treeWidget.expandAll()
        self.setup_tree()
        self.table_widget()
        self.connect_tree_signals()
        self.search()
        
        
    def search(self):
        search_input =self. ui.search
        search_input.setPlaceholderText("검색하기") 
        search_input.setStyleSheet("""
        QLineEdit {
            border: none;                  /* 테두리 제거 */
            background: transparent;       /* 배경을 투명으로 설정 */
            color: white;                  /* 글자 색상을 흰색으로 설정 */
            font-family: 'Pretendard';     /* 폰트는 Pretendard로 설정 */
            font-weight: light;            /* 폰트 두께를 light로 설정 */
            font-size: 13px;               /* 폰트 크기는 11px */
        }
    """)



    def main_ui_setting(self):
        """
        메인 UI 설정
        - 토글 버튼의 toggle의 디폴트 상태를 인스턴스 변수로 정의한다.
        - 토글 버튼에 토글 이미지를 설정/ 디폴트 이미지는 toggle_open.png
        - 메인 ui의 이미지 bg.png 배경으로 설정
        """
        self.like_active =False
        self.toggle_open =QPixmap("./source/toggle_open.png")
        self.toggle_like = QPixmap("./source/toggle_like.png")

        self.ui.toggle_btn.setPixmap(self.toggle_open) 
        bg =QPixmap("./source/bg.png")
        self.ui.label.setPixmap(bg)

        self.ui.toggle_btn_touch_area.clicked.connect(self.toggle_chage) # 토글 버튼 토글 이벤트



    def toggle_chage(self):
        """
        토글 버튼 토글 이벤트
        - 토글 버튼의 toggle의 현재 상태에 따른 이미지 변경
        - true -> false 시 toggle_open, false -> true 시 toggle_like
        """

        if self.like_active == False:
            self.ui.toggle_btn.setPixmap(self.toggle_like)
            self.like_active = True
        else:
            self.ui.toggle_btn.setPixmap(self.toggle_open)
            self.like_active = False

        


    def setup_tree(self):
        """기존 트리 위젯에 체크박스를 추가 (부모 제외, 자식만 추가)"""
        root = self.ui.treeWidget.invisibleRootItem()  # 트리 위젯의 최상위 항목(root item)을 반환하는 treeWidget 객체의 메서드

        for i in range(root.childCount()):  # 최상위 항목의 자식 갯수를 가져오는 메서드
            parent = root.child(i)    #이때 실제 내가 설정한 부모 항목이 변수에 담김
            # print(parent.text(0))  #열과 행이 존재하기 때문에 지정을 해줘야 출력이 가능
            for j in range(parent.childCount()):  # 부모의 자식 항목(Child)
                child = parent.child(j)
                # print(child.text(0))
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)  # 체크박스를 만들수 있는 QT 기능 플래그를 child의 플래그에 추가
                child.setCheckState(0, Qt.Unchecked) #


    def tree_widget(self):
        """
        트리 위젯 스타일 시트 설정
        
        - 항목 간 간격을 조절 (padding: 8px, height: 20px)
        - 배경색을 투명하게 설정 (background: transparent)
        - 테두리를 지워줌 (border: none)
        """
        self.ui.treeWidget.setStyleSheet("""

            /*항목 간 간격을 조절하는 부분*/
            QTreeWidget::item {
                color: white;
                padding: 8px;  /* 항목 간 여백 추가 */
                height: 20px;  /* 항목 높이 조절 */

            }
            QTreeWidget {
            background: transparent;
            border: none;
            }
            """)
        
        
    def connect_tree_signals(self):
        
        """기존 트리 항목에 클릭 시 체크박스를 토글하는 이벤트 연결"""
        self.ui.treeWidget.itemClicked.connect(self.toggle_checkbox)

      
    def toggle_checkbox(self, item, column):
        """트리 항목 클릭 시 체크 상태 토글"""
        if item.flags() & Qt.ItemIsUserCheckable:  # 체크박스가 있는 항목인지 확인
            current_state = item.checkState(column)
            new_state = Qt.Checked if current_state == Qt.Unchecked else Qt.Unchecked
            item.setCheckState(column, new_state)  # 체크박스 상태 변경
        
    


    def table_widget(self):
        
        assets = [
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"},
            {"thumbnail": "./source/asset_sum/thumbnail_abyssal_pipes_column_trim_default.png"}
        ]



        self.ui.tableWidget.horizontalHeader().setVisible(False)  # 열(가로) 헤더 숨기기
        self.ui.tableWidget.verticalHeader().setVisible(False)  # 행(세로) 헤더 숨기기

        max_columns = 5  # 한 줄에 최대 5개 배치
        rows = (len(assets) / max_columns +1)   # 행 개수 계산

        self.ui.tableWidget.setRowCount(rows)  # 행 개수 설정
        self.ui.tableWidget.setColumnCount(max_columns)  # 열 개수 설정

        for index, asset in enumerate(assets):
            row_index = index // max_columns  # index 항목이 몇 번째 행(row)에 있는 정의
            col_index = index % max_columns   # 나머지를 통해 몇번째 열에 있는지 정의
            self.add_thumbnail(row_index, col_index, asset["thumbnail"])

        



    def add_thumbnail(self, row, col, thumbnail_path):

        widget = QWidget()  # 셀 안에 넣을 위젯 생성
        layout = QVBoxLayout()  # 세로 정렬을 위한 레이아웃 생성
        layout.setContentsMargins(0, 0, 0, 10)  # 여백 제거
        layout.setAlignment(Qt.AlignTop)

        Thum = QLabel()
        name = QLabel()
        type = QLabel()

        layout.addWidget(Thum)
        layout.addWidget(name)
        layout.addWidget(type)

        widget.setLayout(layout)  # 위젯에 레이아웃 설정

    


        pixmap = QPixmap(thumbnail_path)
        if pixmap.isNull():
            print(f"❌ 이미지 로드 실패: {thumbnail_path}")

        Thum.setPixmap(pixmap)
        Thum.setFixedHeight(160)

        
        Thum.setAlignment(Qt.AlignCenter)
        

 
        name.setText("name")
        name.setAlignment(Qt.AlignCenter)
        type.setText("type")

        name.setStyleSheet("""
            color: white;                 /* 글자 색상 */
            font-family: 'Pretendard';          /* 글꼴 */
            font-size: 14px;              /* 글자 크기 */
            font-weight: Thin;            /* 글자 굵기 */
        """)


        name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        name.setFixedHeight(14)
        name.setAlignment(Qt.AlignCenter)


        type.setStyleSheet("color: white;")
        type.setStyleSheet("""
            color: white;                 /* 글자 색상 */
            font-family: 'Pretendard';          /* 글꼴 */
            font-size: 12px;              /* 글자 크기 */
            font-weight: light;            /* 글자 굵기 */
        """)
        type.setAlignment(Qt.AlignCenter)
        
        type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        type.setFixedHeight(18)



        self.ui.tableWidget.setCellWidget(row, col, widget)  # 행과 열에 이미지 추가
        self.ui.tableWidget.resizeRowsToContents() 

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
