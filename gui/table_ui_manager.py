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
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl
from ui_loader import UILoader   

# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from assetmanager import AssetService  # AssetService 임포트
from assetmanager import ClickableLabel

from PySide6.QtCore import QObject, QEvent, Qt
from constant import *
# from add_video_player import *

from emitter_class import EmitterParent
from like_state import LikeState

from asset import Asset
from check import Check
from subwin import SubWin
from dynamic_circle_label import DynamicCircleLabel
from logger import *
from download_manager import DownloadManager
from json_manager import DictManager
from bson import ObjectId
from ui_loader import UILoader   

class TableUiManager:
    _instance = None  # 싱글톤 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TableUiManager, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # 중복 초기화를 방지
            super().__init__()
            ui_loader = UILoader("/home/rapa/NA_Spirit/gui/asset_main2.ui")
            self.ui = ui_loader.load_ui()
            self.ui.show()

            self.ui.comboBox.currentTextChanged.connect(self.set_sorting_option)
            self._initialized = True  # 인스턴스가 초기화되었음을 표시
            self.search_word =None
            self.ui.exit_btn.clicked.connect(self.exit_sub_win)
            self.ui.image_l_btn.clicked.connect(partial (SubWin.prev_slide, self.ui.stackedWidget_2))
            self.ui.image_r_btn.clicked.connect(partial (SubWin.next_slide, self.ui.stackedWidget_2))
            self.ui.toggle_btn_touch_area.clicked.connect(self.toggle_change) # 토글 버튼 토글 이벤트
            self.ui.like_btn.clicked.connect(self.toggle_like_icon)
            self.ui.search.textEdited.connect(self.search_input)
            download_manager=DownloadManager()
            

# 버튼 이벤트 연결 (추가 인자 없이 호출)
            self.ui.download_touch_area.clicked.connect(download_manager.download_likged_assets_all)
            
            self.ui.download_btn.clicked.connect(download_manager.download_likged_assets_all)

            self.logger = create_logger(UX_Like_ASSET_LOGGER_NAME, UX_Like_ASSET_LOGGER_DIR)

            self._initialized = True  # 인스턴스가 초기화되었음을 표시
            self.asset_dict = {}

    def search_input(self, search_word):
        self.search_word = search_word
        self.update_table()

#라벨 초기화 함수 실행
    def remove_lable(self):

        while self.ui.image_widget_s.count() > 0:
            item = self.ui.image_widget_s.takeAt(0)
            if item.widget():
                item.widget().deleteLater()  # QLabel 메모리 해제

      
        for label in self.ui.stackedWidget_2.findChildren(QLabel):
            label.deleteLater()

        while self.ui.image_widget_s.count() > 0:
            item = self.ui.image_widget_s.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        #  기존 stackedWidget_2 내부의 QLabel 삭제
        for label in self.ui.stackedWidget_2.findChildren(QLabel):
            label.deleteLater()

        #  기존 stackedWidget_2 내부의 QVideoWidget 삭제
        for video_widget in self.ui.stackedWidget_2.findChildren(QVideoWidget):
            video_widget.deleteLater()

        #  비디오 플레이어 리스트도 정리
        self.video_widgets = []
        self.video_players = []

    def make_label_list(self, list_len): 
        self.remove_lable()
        self.make_labels = []  # 리스트 초기화

        for _ in range(list_len):  
            label = QLabel()
            label.setFixedSize(60, 60)
            label.setAlignment(Qt.AlignCenter)
            self.ui.image_widget_s.addWidget(label)  # 레이아웃에 QLabel 추가
            self.make_labels.append(label)

    def make_video_label_list(self, list_len):
        ui = self.ui  # UI 객체 참조
        print(f"여기 리스트 랜의 갯수를 알려줍니당 {list_len}")

        # 기존 image_widget_s 내부의 위젯 삭제
        while ui.image_widget_s.count() > 0:
            item = ui.image_widget_s.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        #  기존 stackedWidget_2 내부의 QVideoWidget 삭제
        for widget in ui.stackedWidget_2.findChildren(QVideoWidget):
            widget.deleteLater()

        self.make_video_labels = []  # 리스트 초기화
        self.video_players = []  # QMediaPlayer 객체 리스트

        # 새로운 QVideoWidget 추가
        for _ in range(list_len):  
            video_widget = QVideoWidget(ui.stackedWidget_2)  # 부모 설정
            video_widget.setGeometry(0, 0, 380, 291)  #  위치 (0, 53) 크기 (380x291) 설정
            video_widget.show()  # 반드시 show() 호출해야 표시됨

            player = QMediaPlayer()
            player.setVideoOutput(video_widget)

            #  UI 레이아웃에 추가하지 않고 직접 위치 설정했으므로 addWidget() 호출 필요 없음

            #  리스트에 저장
            self.make_video_labels.append(video_widget)
            self.video_players.append(player)

        print(" 비디오 위젯 생성 완료")



    def set_sorting_option(self, option):
        #유저가 설정한 sorting_option에 맞게 table에 적절한 인자를 전달하여 테이블 위젯의 나열순서를 정함
        if option == "오래된 순":
            print(f"오래된 순의 필터임 :{Check().dict}")
            self.update_table(CREATED_AT, 40, 0,None)

        elif option =="다운로드 순":
            print("다운로드된 순서를 정렬할게요")
            self.update_table(DOWNLOADS, 40, 0,None)

        else:
            print("최신 순서를 정렬할게요")
            self.update_table(UPDATED_AT, 40, 0, None)
        
        
    
    def update_table(self, filter_conditions=None, sort_by=None, limit=None, skip=0, fields=None):
        ui = self.ui

        ui.like_empty_notice.hide()
        search_word = self.search_word
        if self.search_word is not None:
            if len(self.search_word) < 3:
                search_word =None
        filter_conditions = {}
        if LikeState().state:
            filter_conditions[OBJECT_ID] = LikeState().like_filter_condition[OBJECT_ID]
        if Check().dict:
            for key, value in Check().dict.items():
                filter_conditions[key] = value

        # if filter_conditions == list:
        #     AssetService.get_asset_by_id_all(filter_conditions, sort_by, limit, skip, search_word)
            
        assets  = list(AssetService.get_all_assets(filter_conditions, sort_by, limit, skip,search_word)) # 모두 가져올거기 때문에 filter_conditions 는 빈딕셔너리
        # print(f"여기에 테이블위젯 구정하는 assets 들어있어요 <<>>>>>>{assets}")

        self.ui.tableWidget.clear()
        self.make_table(assets)

        filter_conditions = None
    
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
        thumbnail_path = asset[PREVIEW_URL]
        asset_name = asset[NAME] 
        aseet_type = asset[ASSET_TYPE]

        widget = QWidget()  # 셀 안에 넣을 위젯 생성
        layout = QVBoxLayout()  # 세로 정렬을 위한 레이아웃 생성
        layout.setContentsMargins(0, 0, 0, 10)  # 여백 제거
        layout.setAlignment(Qt.AlignTop)

        #asset[]#여기에 찾을 항목 적어서 값 도출  

        Thum = ClickableLabel("썸네일", parent=widget)
        name = ClickableLabel("이름", parent=widget)
        type = ClickableLabel("타입", parent=widget)

        Thum.clicked.connect(lambda: self.set_detail_info(asset))
        name.clicked.connect(lambda: self.set_detail_info(asset))
        type.clicked.connect(lambda: self.set_detail_info(asset))

        layout.addWidget(Thum)
        layout.addWidget(name)
        layout.addWidget(type)

        widget.setLayout(layout)  # 위젯에 레이아웃 설정

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

    def set_detail_info(self, asset):
        Asset().current = asset
        ui=self.ui
        ui.stackedWidget.show()
        detail_thum_urls=[]
        
        try:
            self.timer.stop()
        except:
            pass
        
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

            for url in asset["image_url"]:
                detail_thum_urls.append(url)
          
      

        elif asset[ASSET_TYPE]=="3D Model":
            
            for url in asset["video_url"]:
                detail_thum_urls.append(url)
            
            print(detail_thum_urls)
      

        elif asset[ASSET_TYPE]=="HDRI":
            for url in asset["image_url"]:
                detail_thum_urls.append(url)
   

        else:
            for url in asset["image_url"]:
                detail_thum_urls.append(url)
               
            
          
        self.make_label_list(len(detail_thum_urls))
        SubWin.show_asset_detail_image(self.ui.stackedWidget_2,detail_thum_urls, self.make_labels)



            
    def toggle_like_icon(self):
        """하트 버튼을 누르는 시그널로 실행
        아이콘 변경 & 딕셔너리에 좋아요한 asset 정보 저장 """

        like_state = LikeState()
        asset = Asset().current
        asset_object_id = str(asset[OBJECT_ID])
  

        
    
        current_icon = self.ui.like_btn.icon()
     
        if current_icon.cacheKey() == like_state.like_icon_empty.cacheKey():  #빈하트 상태일때 
            self.ui.like_btn.setIcon(like_state.like_icon)
            print("여기에요여기~~~"+asset_object_id)
            like_state.like_asset_list.append(asset_object_id)
            self.logger.info(f"유저가 {asset[NAME]} 에셋을 관심리스트에 추가했습니다\n해당 에셋 정보 : {asset}")
            DictManager().save_dict_to_json(like_state.like_asset_list)
            
  
            

            if LikeState().state == True:
                print("저 서브바가 열려있을때만 닫혀요")
                self.ui.tableWidget.clear()
                self.update_table(sort_by=UPDATED_AT, limit=40, skip=0,fields=None)
                self.ui.like_download_btn.show()
                self.ui.like_download_btn_area.show()

         
            
      
            
            
                
        else:  # 채워진 하트 상태일 때 (좋아요 취소)
            print("하트 지워짐")
            self.ui.like_btn.setIcon(like_state.like_icon_empty)  # 빈 하트로 변경
            if asset_object_id in like_state.like_asset_list:
                index = like_state.like_asset_list.index(asset_object_id)
                remove_asset=like_state.like_asset_list.pop(index)  # 리스트에서 제거
                self.logger.info(f"유저가 {asset[NAME]} 에셋을 관심리스트에서 삭제했습니다\n해당 에셋 정보 : {remove_asset}")
                print(f"유저가 {asset[NAME]} 에셋을 관심리스트에서 삭제했습니다\n해당 에셋 정보 : {remove_asset}")
                DictManager.save_dict_to_json(like_state.like_asset_list)

            if LikeState().state == True:
                print("저 서브바가 열려있을때만 닫혀요")
                self.ui.tableWidget.clear()
                self.update_table(sort_by=UPDATED_AT, limit=40, skip=0,fields=None)
                self.ui.like_download_btn.show()
                self.ui.like_download_btn_area.show()
          
                
                
        like_state.set_like_icon(asset_object_id, self.ui.like_btn)

    def toggle_change(self): 
        """토글 버튼 변경 이벤트 - 내부 위젯도 삭제"""

        # ✅ 기존 위젯 삭제 (내부 요소 포함)
        self.clear_layout(self.ui.like_asset_number)

        if LikeState().state == False:
            self.ui.toggle_btn.setPixmap(LikeState().toggle_like)
            
            LikeState().state = True
            if not LikeState().like_asset_list:
                self.ui.tableWidget.clear()
                self.ui.like_empty_notice.show()
                
            else:
                self.ui.tableWidget.clear()
                self.update_table(sort_by=UPDATED_AT, limit=40, skip=0,fields=None)
                self.ui.like_download_btn.show()
                self.ui.like_download_btn_area.show()

                # ✅ 새로운 DynamicCircleLabel 추가
                label = DynamicCircleLabel(str(len(LikeState().like_asset_list)))
                self.ui.like_asset_number.addWidget(label)  #  새로운 라벨 추가
                
                self.ui.like_download_btn.setPixmap(LikeState().like_download_image)

                self.ui.like_empty_notice.hide()
        else: 
            self.ui.like_download_btn.hide()
            self.ui.like_download_btn_area.hide()
            if LikeState().state == True:
                self.ui.toggle_btn.setPixmap(LikeState().toggle_open)
                LikeState().state = False
                self.ui.like_empty_notice.hide()
                self.ui.tableWidget.clear()
                self.update_table(sort_by=UPDATED_AT, limit=40, skip=0,fields=None)
                #사용자 pc에 저장해두고 라이크 받을때 마다 오브젝트 id를 json에 저장해두고 

    def remove_widget_with_children(self,widget):
        """위젯과 그 내부 요소 삭제"""
        if widget is not None:
            layout = widget.layout()  # ✅ 위젯에 레이아웃이 있는 경우 가져오기
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    child_widget = item.widget()
                    if child_widget:
                        child_widget.deleteLater()  # ✅ 내부 요소 삭제
            widget.setParent(None)  # ✅ 부모에서 제거
            widget.deleteLater()  # ✅ 위젯 자체도 삭제

    def clear_layout(self, layout):
        """레이아웃 내부의 모든 요소 삭제"""
        while layout.count():  # 레이아웃에 위젯이 남아있는 동안 반복
            item = layout.takeAt(0)  # 첫 번째 아이템 가져오기
            widget = item.widget()  # 아이템이 위젯인지 확인
            if widget is not None:
                widget.setParent(None)  # ✅ 부모에서 제거
                widget.deleteLater()  # ✅ 메모리에서 완전 삭제


    