# 로거 파일 추가해서 유저가 중요한 
##### json 파일은 나스피릿에 넣고 이그노어 에 포함

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget,QGraphicsOpacityEffect
from PySide6.QtCore import QFile, Qt, Signal, QEvent, QObject, QUrl
from PySide6.QtGui import QPixmap, QPixmap, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QSizePolicy ,QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
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
from constant import *
# from add_video_player import *

from emitter_class import EmitterParent
from like_state import LikeState

from asset import Asset
from check import Check

class TableUiManager:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TableUiManager, cls).__new__(cls)

        return cls._instance

    def __init__(self,ui):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            super().__init__()
            self.ui = ui
            self.ui.comboBox.currentTextChanged.connect(self.set_sorting_option)
            self._initialized = True  # 인스턴스가 초기화되었음을 표시

            self.ui.exit_btn.clicked.connect(self.exit_sub_win)
            self.ui.image_l_btn.clicked.connect(self.prev_slide)
            self.ui.image_r_btn.clicked.connect(self.next_slide)




            self.image_labels = []
            self.make_label_list()

            self.ui.toggle_btn_touch_area.clicked.connect(self.toggle_change) # 토글 버튼 토글 이벤트
            self.ui.like_btn.clicked.connect(self.toggle_like_icon)

            self._initialized = True  # 인스턴스가 초기화되었음을 표시

    def make_label_list(self): 
        for _ in range(4):  # 4개의 QLabel을 미리 생성
            label = QLabel()
            label.setFixedSize(60, 60)
            label.setAlignment(Qt.AlignCenter)
            self.ui.image_widget_s.addWidget(label)  # 초기 레이아웃에 QLabel 추가
            self.image_labels.append(label)

    def set_sorting_option(self, option):
            #유저가 설정한 sorting_option에 맞게 table에 적절한 인자를 전달하여 테이블 위젯의 나열순서를 정함
            if option == "오래된 순":
                print(f"오래된 순의 필터임 :{Check().dict}")
                self.table_widget(Check().dict,UPDATED_AT, 40, 0,None)

            elif option =="다운로드 순":
                print("다운로드된 순서를 정렬할게요")
                self.table_widget(Check().dict,DOWNLOADS, 40, 0,None)

            else:
                print("최신 순서를 정렬할게요")
                self.table_widget(Check().dict,CREATED_AT, 40, 0, None)

    
    def table_widget(self, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        ui = self.ui
        # 리뷰 이거 셀프로 init에 구현 이거 근데 저장하는 변수명이 쫌...... 
        # 리뷰 static밖에 없는데 왜 객체 생성????
        ui.like_empty_notice.hide()
    
        assets = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip)) # 모두 가져올거기 때문에 filter_conditions 는 빈딕셔너리
        print(f"asset입니다 >>>>>>> {assets}")
        self.make_table(assets)
    
    def make_table(self, assets):
        ui = self.ui
        len_asset =len(assets)
        ui.tableWidget.horizontalHeader().setVisible(False)  # 열(가로) 헤더 숨기기
        ui.tableWidget.verticalHeader().setVisible(False)  # 행(세로) 헤더 숨기기

        max_columns = 5  # 한 줄에 최대 5개 배치

        rows = (len_asset / max_columns +1)   # 행 개수 계산

        ui.tableWidget.setRowCount(rows)  # 행 개수 설정
        ui.tableWidget.setColumnCount(max_columns)  # 열 개수 설정

        for index, asset in enumerate(assets):
            row_index = index // max_columns  # index 항목이 몇 번째 행(row)에 있는 정의
            col_index = index % max_columns   # 나머지를 통해 몇번째 열에 있는지 정의
            self.add_thumbnail(row_index, col_index, asset)

    def add_thumbnail(self, row, col, asset):
        ui = self.ui
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

        ui.tableWidget.setCellWidget(row, col, widget)  # 행과 열에 이미지 추가
        ui.tableWidget.resizeRowsToContents() 

    def exit_sub_win(self):
        
        self.ui.stackedWidget.hide()

    def del_label(self, asset):

        Asset().current = asset
        ui=self.ui
        """라벨 클릭 이벤트 발생 시 실행"""
        
       # 기존 라벨 개수 확인
        for label in ui.image_widget_s.findChildren(QWidget):
            print(f" QLabel 위치 확인: {label} (부모: {label.parent()})")

        try:
            for label in ui.stackedWidget_2.findChildren(QLabel):
                label.deleteLater()

            self.set_detail_info(asset)

        except TypeError:
            # set_detail_info(asset)
            print("error")


    def set_detail_info(self, asset):
        ui=self.ui
        ui.stackedWidget.show()
        detail_thum_urls=[]
        
        # for asset_id, asset_info in asset.items(): 
        LikeState().set_like_icon(str(asset[OBJECT_ID]),self.ui.like_btn)
        
        Asset().current= asset
        ui.info_name.setText(asset[NAME])
        ui.info_name_2.setText(asset[NAME])
        ui.description.setText(asset[DESCRIPTION])
        ui.asset_type.setText(asset[ASSET_TYPE])
        ui.creator.setText(f"담당 직원 : {asset[CREATOR_NAME]} ( ID : {asset[CREATOR_ID]} )")
        ui.downloads.setText(f"다운로드 횟수 : {asset[DOWNLOADS]}회")
        ui.create_at.setText(f"최초 생성일 : {asset[CREATED_AT]}회")
        ui.update_up.setText(f"최종 수정일 : {asset[UPDATED_AT]}회")

        #세부항목 태그
        common_style = "color: #ffffff; background-color: #282828; padding: 5px; border-radius: 12px;"

        # QLabel 목록과 해당할 데이터 매핑
        labels = {
            ui.category: asset[CATEGORY],
            ui.style_area: asset[STYLE],
            ui.license_type: asset[LICENSE_TYPE],
        }

        # 반복문을 사용해 설정 적용
        for label, text in labels.items():
            label.setText(text)
            label.setStyleSheet(common_style)
            label.adjustSize()

        # 이미지 URL 가져오기
        if asset[ASSET_TYPE]=="Texture":
            print(f"에셋 타입 >>>>>>>>{asset[ASSET_TYPE]}")
            detail_thum_urls = [
                asset["detail_url"],
                asset["presetting_url1"],
                asset["presetting_url2"],
                asset["presetting_url3"]
            ]
            self.show_asset_detail_image(detail_thum_urls)

        elif asset[ASSET_TYPE]=="3D Model":
            detail_thum_urls = [
                asset["turnaround_url"],
                asset["rig_url"]
            ]
            # SubWinUiManager.show_asset_detail_media(ui,detail_thum_urls)

        elif asset[ASSET_TYPE]=="3D Model":
            detail_thum_urls = [
                asset["applyhdri_url"],
                asset["hdri_url"]
            ]
            self.show_asset_detail_image(detail_thum_urls)


    def show_asset_detail_image(self, detail_thum_urls):
        ui = self.ui
        for img_path in detail_thum_urls:
            if img_path == None:
                continue
            label = QLabel()
            pixmap = QPixmap(img_path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            ui.stackedWidget_2.addWidget(label)

        for idx, label in enumerate(self.image_labels):
            if idx < len(detail_thum_urls) and detail_thum_urls[idx]:  # URL이 있는 경우에만 설정
                pixmap = QPixmap(detail_thum_urls[idx])
                label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                label.clear()
        
        ui.stackedWidget_2.setCurrentIndex(0)  # 0번째의 label을 보여준다. 


    
    def next_slide(self):
        """다음 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        next_index = (current_index + 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(next_index)
        print(f"{next_index}다음 이미지로 변경됨")
      
    def prev_slide(self):
        """이전 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        prev_index = (current_index - 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(prev_index)
        print("이전 이미지로 변경됨")
      # 리뷰 순서를 정리를 


            
            
    def toggle_like_icon(self):
        """하트 버튼을 누르는 시그널로 실행
        아이콘 변경 & 딕셔너리에 좋아요한 asset 정보 저장 """
     
        asset = Asset().current
        asset_object_id = str(asset[OBJECT_ID])
        current_icon = self.ui.like_btn.icon()
        if current_icon.cacheKey() == LikeState().like_icon_empty.cacheKey():  #빈하트 상태일때 
            self.ui.like_btn.setIcon(LikeState().like_icon)
            LikeState().like_asset_list.append(asset_object_id)
           
                
        else:  # 채워진 하트 상태일 때 (좋아요 취소)
            self.ui.like_btn.setIcon(LikeState().like_icon_empty)  # 빈 하트로 변경
            if asset_object_id in LikeState().like_asset_list:
                index = LikeState().like_asset_list.index(asset_object_id)
                LikeState().like_asset_list.pop(index)  # 리스트에서 제거
                
        LikeState().set_like_icon(asset_object_id, self.ui.like_btn)



    def toggle_change(self): 

        """
        토글 버튼 토글 이벤트
        - 토글 버튼의 toggle의 현재 상태에 따른 이미지 변경
        - true -> false 시 toggle_open, false -> true 시 toggle_like
        """

        if LikeState().state == False:
            self.ui.toggle_btn.setPixmap(LikeState().toggle_like)
            LikeState().state = True
            if not LikeState().like_asset_list:
                self.ui.tableWidget.clear()
                self.ui.like_empty_notice.show()
                
            else:
                self.ui.tableWidget.clear()
                like_asset_dict = []
                for object_id in LikeState().like_asset_list:
                    asset_info = AssetService.get_asset_by_id(object_id)
                    like_asset_dict.append(asset_info)
                    
                self.make_table(like_asset_dict)
                self.ui.like_empty_notice.hide()
        else: 
            if LikeState().state == True:
                self.ui.toggle_btn.setPixmap(LikeState().toggle_open)
                LikeState().state = False
                self.ui.like_empty_notice.hide()
                self.ui.tableWidget.clear()
                self.table_widget(Check().dict,UPDATED_AT, 40, 0,None)
                #사용자 pc에 저장해두고 라이크 받을때 마다 오브젝트 id를 json에 저장해두고 