class EventHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = None  # UI 매니저가 설정된 후 초기화됨
        self.check_dict = {}

    def connect_events(self):
        """UI 이벤트 연결"""
        self.ui = self.main_window.ui_manager.ui  # UI 객체를 여기서 가져오기
        if not self.ui:
            raise AttributeError("UI가 로드되지 않았습니다. UiManager에서 올바르게 설정되었는지 확인하세요.")
        
        self.ui.exit_btn.clicked.connect(self.exit_sub_win)
        self.ui.toggle_btn_touch_area.clicked.connect(self.toggle_change)
        self.ui.treeWidget.itemClicked.connect(self.toggle_checkbox)
        self.ui.image_l_btn.clicked.connect(self.prev_slide)
        self.ui.image_r_btn.clicked.connect(self.next_slide)
        self.ui.comboBox.currentTextChanged.connect(self.set_sorting_option)
        self.ui.like_btn.clicked.connect(self.toggle_like_icon)

    def exit_sub_win(self):
        self.ui.stackedWidget.hide()
    
    def toggle_change(self):
        """토글 버튼 상태 변경"""
        if self.ui.toggle_btn.pixmap().cacheKey() == self.main_window.ui_manager.ui.toggle_open.cacheKey():
            self.ui.toggle_btn.setPixmap(self.main_window.ui_manager.ui.toggle_like)
        else:
            self.ui.toggle_btn.setPixmap(self.main_window.ui_manager.ui.toggle_open)

    def prev_slide(self):
        """이전 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        prev_index = (current_index - 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(prev_index)
    
    def next_slide(self):
        """다음 슬라이드 이동"""
        current_index = self.ui.stackedWidget_2.currentIndex()
        next_index = (current_index + 1) % self.ui.stackedWidget_2.count()
        self.ui.stackedWidget_2.setCurrentIndex(next_index)
    
    def set_sorting_option(self, option):
        """정렬 옵션 변경"""
        if option == "오래된 순":
            self.main_window.asset_manager.load_assets(sort_by="UPDATED_AT")
        elif option == "다운로드 순":
            self.main_window.asset_manager.load_assets(sort_by="DOWNLOADS")
        else:
            self.main_window.asset_manager.load_assets(sort_by="CREATED_AT")
    
    def toggle_checkbox(self, item, column):
        """트리 항목 클릭 시 체크 상태 토글"""
        self.ui.tableWidget.clear()
        if item.flags() & Qt.ItemIsUserCheckable:  # item이 체크 가능 여부 확인
            current_state = item.checkState(column)
            new_state = Qt.Checked if current_state == Qt.Unchecked else Qt.Unchecked
            item.setCheckState(column, new_state)
            
            filter_name_convert = str(item.text(0))
            parent_name = item.parent()
            if parent_name:
                parent_item_convert = parent_name.text(0)
                if parent_item_convert == "Asset":
                    parent_item_convert = "asset_type"
                elif parent_item_convert == "Category":
                    parent_item_convert = "category"
                else:
                    parent_item_convert = "style"
                
                if new_state == Qt.Checked:
                    self.check_dict.setdefault(parent_item_convert, []).append(filter_name_convert)
                else:
                    self.check_dict[parent_item_convert].remove(filter_name_convert)
                    if not self.check_dict[parent_item_convert]:
                        del self.check_dict[parent_item_convert]
            
            sort_by = self.ui.comboBox.currentText()
            if sort_by == "최신 순":
                sort_by = "CREATED_AT"
            elif sort_by == "오래된 순":
                sort_by = "UPDATED_AT"
            else:
                sort_by = "DOWNLOADS"
            
            self.main_window.asset_manager.load_assets(filter_conditions=self.check_dict, sort_by=sort_by)
    
    def toggle_like_icon(self):
        """하트 버튼 클릭 시 아이콘 변경 및 좋아요 리스트 업데이트"""
        asset = self.main_window.asset_manager.current_asset
        current_icon = self.ui.like_btn.icon()
        
        if current_icon.cacheKey() == self.main_window.ui_manager.like_icon_empty.cacheKey():
            self.ui.like_btn.setIcon(self.main_window.ui_manager.like_icon)
            self.main_window.asset_manager.like_asset_list.append(str(asset["OBJECT_ID"]))
        else:
            self.ui.like_btn.setIcon(self.main_window.ui_manager.like_icon_empty)
            if str(asset["OBJECT_ID"]) in self.main_window.asset_manager.like_asset_list:
                self.main_window.asset_manager.like_asset_list.remove(str(asset["OBJECT_ID"]))
        
        self.set_like_icon(asset)
    
    def set_like_icon(self, asset):
        """현재 에셋의 좋아요 상태에 따라 아이콘 설정"""
        if str(asset["OBJECT_ID"]) in self.main_window.asset_manager.like_asset_list:
            self.ui.like_btn.setIcon(self.main_window.ui_manager.like_icon)
        else:
            self.ui.like_btn.setIcon(self.main_window.ui_manager.like_icon_empty)
