from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget,QGraphicsOpacityEffect
from PySide6.QtCore import QFile, Qt, Signal, QEvent, QObject
from PySide6.QtGui import QPixmap, QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy ,QVBoxLayout
from functools import partial
import sys
import os
# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from asset_service import AssetService  # AssetService 임포트
from asset_service import ClickableLabel

from PySide6.QtCore import QObject, QEvent, Qt
from db_constant import *

class MainUi(QMainWindow):
    clicked = Signal()
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.image_labels = [] 
        self.make_label_list()
        self.tree_widget()
        self.main_ui_setting()
        self.user_num()
        self.ui.treeWidget.expandAll()
        self.add_tree_checkbox()
        self.table_widget(None,UPDATED_AT, 50, 0,None)
        self.connect_tree_signals()
        self.set_search_area_design()
        self.ui.exit_btn.clicked.connect(self.exit_sub_win)
        self.check_dict = {}    
        self.like_asset_dict = {}

        self.sub_bar = False

  

    def make_label_list(self):
         

        for _ in range(4):  # 4개의 QLabel을 미리 생성
            label = QLabel()
            label.setFixedSize(60, 60)
            label.setAlignment(Qt.AlignCenter)
            self.ui.image_widget_s.addWidget(label)  # 초기 레이아웃에 QLabel 추가
            self.image_labels.append(label)
    
    def exit_sub_win(self):
        
        self.ui.stackedWidget.hide()

        
    
    def get_checked_items(self):
        """QTreeWidget에서 체크된 항목들의 텍스트를 가져오는 함수"""
        checked_items = []  # 체크된 항목을 저장할 리스트
        root = self.ui.treeWidget.invisibleRootItem()  # 트리의 루트 아이템 가져오기

        def traverse_tree(item):
            """재귀적으로 트리의 모든 항목을 탐색"""
            for i in range(item.childCount()):
                child = item.child(i)
                if child.checkState(0) == Qt.Checked:  #  체크된 항목 확인
                    checked_items.append(child.text(0))  #  항목의 텍스트 저장
                traverse_tree(child)  #  자식 항목이 있을 경우 재귀적으로 탐색


        traverse_tree(root)  # 트리 탐색 시작

        
        return checked_items
     

        
        
    def set_search_area_design(self):
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

    def toggle_like_icon(self,asset):
        """하트 버튼을 눌렀을때 아이콘 변경 & 딕셔너리에 좋아요한 asset 정보 저장 """
        current_icon = self.ui.like_btn.icon()
        if current_icon.cacheKey() == self.like_icon_empty.cacheKey():
            self.ui.like_btn.setIcon(self.like_icon)
            for asset_id, asset_info in asset.items(): 
                self.like_asset_dict[asset_id]=asset_info
                print(f"여기 좋아요한 에셋이 어떻게 담겼는지 나와요 >>> {self.like_asset_dict}")
        else:
            self.ui.like_btn.setIcon(self.like_icon_empty)
            for asset_id, asset_info in asset.items(): 
                del self.like_asset_dict[asset_id]
                print(f"여기 좋아요한 에셋이 어떻게 담겼는지 나와요 >>> {self.like_asset_dict}")


    def main_ui_setting(self):

        """
        메인 UI 설정
        - 토글 버튼의 toggle의 디폴트 상태를 인스턴스 변수로 정의한다.
        - 토글 버튼에 토글 이미지를 설정/ 디폴트 이미지는 toggle_open.png
        - 메인 ui의 이미지 bg.png 배경으로 설정
        """
        self.like_icon_empty = QIcon("/nas/spirit/asset_project/source/like_icon.png")
        self.like_icon = QIcon("/nas/spirit/asset_project/source/like_icon_on.png")

        self.ui.like_btn.setIcon(self.like_icon_empty)
       

        self.like_active =False
        self.toggle_open =QPixmap("/nas/spirit/asset_project/source/toggle_open.png")
        self.toggle_like = QPixmap("/nas/spirit/asset_project/source/toggle_like.png")

        info_list_bar_s=QPixmap("/nas/spirit/asset_project/source/info_list_bar.png")
        self.ui.info_list_bar_s.setPixmap(info_list_bar_s)
    
        self.ui.toggle_btn.setPixmap(self.toggle_open) 
        bg =QPixmap("/nas/spirit/asset_project/source/bg.png")
        
        self.ui.label.setPixmap(bg)

        self.ui.toggle_btn_touch_area.clicked.connect(self.toggle_change) # 토글 버튼 토글 이벤트

        #사이드 바 기본 설정 
        
        

        self.ui.stackedWidget.hide()
        self.filter=self.ui.treeWidget.itemClicked.connect(self.get_checked_items)


        # 사이드 바 안에 이미지 롤링 배너 안 stackedwidget에 속한 위젯 지우기
        self.ui.stackedWidget_2.removeWidget(self.ui.page)
        self.ui.stackedWidget_2.removeWidget(self.ui.page_2)

        #정렬 콤보박스를 바꾸면 set_sorting_option 메서드로 연결
        self.ui.comboBox.currentTextChanged.connect(self.set_sorting_option)


    def set_sorting_option(self, option):

        #유저가 설정한 sorting_option에 맞게 table에 적절한 인자를 전달하여 테이블 위젯의 나열순서를 정함
        if option == "오래된 순":
            print(f"오래된 순의 필터임 :{self.check_dict}")
            self.table_widget(self.check_dict,UPDATED_AT, None, 0,None)

        elif option =="다운로드 순":
            print("다운로드된 순서를 정렬할게요")
            self.table_widget(self.check_dict,DOWNLOADS, None, 0,None)

        else:
            print("최신 순서를 정렬할게요")
            self.table_widget(self.check_dict,CREATED_AT, None, 0, None)



    def toggle_change(self): 

        """
        토글 버튼 토글 이벤트
        - 토글 버튼의 toggle의 현재 상태에 따른 이미지 변경
        - true -> false 시 toggle_open, false -> true 시 toggle_like
        """

        if self.like_active == False:
            self.ui.toggle_btn.setPixmap(self.toggle_like)
            self.like_active = True
            self.table_widget(self.like_asset_dict,UPDATED_AT, 50, 0,None)
            
        else:
            self.ui.toggle_btn.setPixmap(self.toggle_open)
            self.like_active = False
            self.table_widget(None,UPDATED_AT, 50, 0,None)

        


    def add_tree_checkbox(self): # 리뷰 메서드 이름  , 변수명
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


    def tree_widget(self): # 리뷰 메서드 이름
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
        
        
    def connect_tree_signals(self): # 한줄 할거면 왜 구현? 모으면서 지워주세요 심지어 커넥트임 
        
        """기존 트리 항목에 클릭 시 체크박스를 토글하는 이벤트 연결"""
        self.ui.treeWidget.itemClicked.connect(self.toggle_checkbox)

      
    def toggle_checkbox(self, item, column): 
        """트리 항목 클릭 시 체크 상태 토글"""
        if item.flags() & Qt.ItemIsUserCheckable:  # item이 체크 가능 여부 확인
            current_state = item.checkState(column)  #item.checkState(column)은 현재 열(column)에 있는 체크 상태를 가져오는 메서드
            new_state = Qt.Checked if current_state == Qt.Unchecked else Qt.Unchecked #체크되어있다면 미체크로, 미체크라면 체크로 상태 변경 

            filter_name_convert =str(item.text(0)) 
            
            #체크박스의 item 문자열을 상수화 시키기
            parent_name = item.parent()
            parent_item_convert=parent_name.text(0)

            #체크박스의 parent 문자열을 db의 key 명과 일치 시키기
            if parent_item_convert == "Asset":
                parent_item_convert = "asset_type"
            elif parent_item_convert == "Category":
                parent_item_convert = "category"
            else: 
                parent_item_convert = "style"


            
        

            print(parent_item_convert)
            print(filter_name_convert)


            item.setCheckState(column, new_state)  # 체크박스 상태 변경
            
            
            if new_state == Qt.Checked:  #체크 상태일 경우 부모 item을 키로 item을 list에 담아 value로 추가
                self.check_dict.setdefault(parent_item_convert, []).append(filter_name_convert)
            else:  #체크 해제 상태일 경우 부모 item의 키에서 해당하는 value 삭제
                self.check_dict[parent_item_convert].remove(filter_name_convert)
                if self.check_dict[parent_item_convert] == []:
                    del self.check_dict[parent_item_convert]
              
           
            sort_by = self.ui.comboBox.currentText()
            if sort_by == "최신 순":
                sort_by=CREATED_AT
            elif sort_by == "오래된 순":
                sort_by = UPDATED_AT
            else:
                sort_by = DOWNLOADS
                

            self.table_widget(filter_conditions = self.check_dict, sort_by= sort_by, limit = 20, skip = 0, fields =None)

            #만들어 진 리스트를 필터로 table에 정렬해주기 + s실제 콤보박스의 정렬이랑도 섞여야함
         

        
    


    def table_widget(self, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        # 리뷰 이거 셀프로 init에 구현 이거 근데 저장하는 변수명이 쫌...... 
        # 리뷰 static밖에 없는데 왜 객체 생성????
        
       
        asset = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip)) # 모두 가져올거기 때문에 filter_conditions 는 빈딕셔너리
        len_asset =len(asset)
        print(f"asset입니다 >>>>>>> {asset}")

        #"file_format", "updated_at", "downloads" << 가지고 있는 정렬 기준



        self.ui.tableWidget.horizontalHeader().setVisible(False)  # 열(가로) 헤더 숨기기
        self.ui.tableWidget.verticalHeader().setVisible(False)  # 행(세로) 헤더 숨기기

        max_columns = 5  # 한 줄에 최대 5개 배치

        rows = (len_asset / max_columns +1)   # 행 개수 계산

        self.ui.tableWidget.setRowCount(rows)  # 행 개수 설정
        self.ui.tableWidget.setColumnCount(max_columns)  # 열 개수 설정

        for index, asset in enumerate(asset):
            row_index = index // max_columns  # index 항목이 몇 번째 행(row)에 있는 정의
            col_index = index % max_columns   # 나머지를 통해 몇번째 열에 있는지 정의
            self.add_thumbnail(row_index, col_index, asset)

    
    def del_label(self, asset):
        """라벨 클릭 이벤트 발생 시 실행"""
       # ✅ 기존 라벨 개수 확인
        
   
        for label in self.ui.image_widget_s.findChildren(QWidget):
            print(f"🔍 QLabel 위치 확인: {label} (부모: {label.parent()})")

        try:
            
            for label in self.ui.stackedWidget_2.findChildren(QLabel):
                label.deleteLater()


            
            self.ui.image_l_btn.clicked.disconnect(self.prev_slide)
            self.ui.image_r_btn.clicked.disconnect(self.next_slide)
            self.set_detail_info(asset)
         

        except TypeError:
            self.set_detail_info(asset)

  
    
    def set_detail_info(self, asset):
        self.ui.like_btn.clicked.connect(partial(self.toggle_like_icon,asset))
        print("이미지 로드 됨")
        self.ui.stackedWidget.show()
        detail_thum_urls=[]
        self.ui.info_name.setText(asset[NAME])
        self.ui.info_name_2.setText(asset[NAME])
        self.ui.description.setText(asset[DESCRIPTION])
        self.ui.asset_type.setText(asset[ASSET_TYPE])
        self.ui.creator.setText(f"담당 직원 : {asset[CREATOR_NAME]} ( ID : {asset[CREATOR_ID]} )")
        self.ui.downloads.setText(f"다운로드 횟수 : {asset[DOWNLOADS]}회")
        self.ui.create_at.setText(f"최초 생성일 : {asset[CREATED_AT]}회")
        self.ui.update_up.setText(f"최종 수정일 : {asset[UPDATED_AT]}회")

        #세부항목 태그

        common_style = "color: #ffffff; background-color: #282828; padding: 5px; border-radius: 12px;"

        # QLabel 목록과 해당할 데이터 매핑
        labels = {
            self.ui.category: asset[CATEGORY],
            self.ui.style_area: asset[STYLE],
            self.ui.license_type: asset[LICENSE_TYPE],
            

         
        }

        # 반복문을 사용해 설정 적용
        for label, text in labels.items():
            label.setText(text)
            label.setStyleSheet(common_style)
            label.adjustSize()





        # 이미지 URL 가져오기
        detail_thum_urls = [
            asset["detail_url"],
            asset["presetting_url1"],
            asset["presetting_url2"],
            asset["presetting_url3"]
        ]
        
        print(detail_thum_urls)
        for img_path in detail_thum_urls:
            label = QLabel()
            pixmap = QPixmap(img_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            self.ui.stackedWidget_2.addWidget(label)
      

        for idx, label in enumerate(self.image_labels):
            if idx < len(detail_thum_urls) and detail_thum_urls[idx]:  # URL이 있는 경우에만 설정
                pixmap = QPixmap(detail_thum_urls[idx])
                label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                label.clear()
        
        self.ui.stackedWidget.setCurrentIndex(0)  # 0번째의 label을 보여준다. 
        
        self.ui.image_l_btn.clicked.connect(self.prev_slide)
        self.ui.image_r_btn.clicked.connect(self.next_slide)

    def next_slide(self):
        """다음 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        next_index = (current_index + 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(next_index)
        print("다음 이미지로 변경됨")
      

    def prev_slide(self):
        """이전 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        prev_index = (current_index - 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(prev_index)
        print("이전 이미지로 변경됨")

      # 리뷰 순서를 정리를 

    def add_thumbnail(self, row, col, asset):
        thumbnail_path = asset["preview_url"]
        asset_name = asset["name"] 
        aseet_type = asset["asset_type"]


        widget = QWidget()  # 셀 안에 넣을 위젯 생성
        layout = QVBoxLayout()  # 세로 정렬을 위한 레이아웃 생성
        layout.setContentsMargins(0, 0, 0, 10)  # 여백 제거
        layout.setAlignment(Qt.AlignTop)

        #asset[]#여기에 찾을 항목 적어서 값 도출

        Thum = ClickableLabel("썸네일", parent=widget)
        name = ClickableLabel("이름", parent=widget)
        type = ClickableLabel("타입", parent=widget)

        Thum.clicked.connect(lambda: self.del_label(asset))
        name.clicked.connect(lambda: self.del_label(asset))
        type.clicked.connect(lambda: self.del_label(asset))

        layout.addWidget(Thum)
        layout.addWidget(name)
        layout.addWidget(type)

        widget.setLayout(layout)  # 위젯에 레이아웃 설정

        # 리뷰 엔터 개 길어


        pixmap = QPixmap(thumbnail_path)
        if pixmap.isNull():
            print(f" 이미지 로드 실패: {thumbnail_path}")

        Thum.setPixmap(pixmap)
        Thum.setFixedHeight(160)

        
        Thum.setAlignment(Qt.AlignCenter)
        

 
        name.setText(asset_name)
        name.setAlignment(Qt.AlignCenter)
        type.setText(aseet_type)

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
            font-weight: Pretendard-ExtraLight;            /* 글자 굵기 */
        """)
        type.setAlignment(Qt.AlignCenter)
        
        type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        type.setFixedHeight(18)



        self.ui.tableWidget.setCellWidget(row, col, widget)  # 행과 열에 이미지 추가
        self.ui.tableWidget.resizeRowsToContents() 

    def user_num(self):
        self.ui.user_num.setText("b976211")

    def load_ui(self):
        ui_file_path = "/home/llly/NA_Spirit/DB/gui/asset_main2.ui"
        ui_file = QFile(ui_file_path)  
        loader = QUiLoader() 
        self.ui = loader.load(ui_file) 

        self.ui.show()  
        ui_file.close()

app = QApplication(sys.argv)
window = MainUi()
app.exec()
