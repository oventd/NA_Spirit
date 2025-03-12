import sys
import os
import re

try:
    from PySide6.QtWidgets import (
        QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem,
        QPushButton, QHeaderView, QCheckBox, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
    )
    from PySide6.QtCore import QFile, Qt
    from PySide6.QtGui import QColor
except ImportError:
    from PySide2.QtWidgets import (
        QMainWindow, QApplication, QWidget, QTableWidget, QTableWidgetItem,
        QPushButton, QHeaderView, QCheckBox, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
    )
    from PySide2.QtCore import QFile, Qt
    from PySide2.QtGui import QColor

import maya.cmds as cmds
import maya.OpenMayaUI as omui
try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken6 import wrapInstance

USD_DIRECTORY = "/home/rapa/maya/version_match"

class VersionCheckUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USD & Maya Version Matching Check")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        """UI 요소 초기화 및 설정"""
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Check Box", "Asset", "Current", "Latest"])

        header = self.table.horizontalHeader()
        
        # 체크박스 열만 크기 자동 조정, 나머지는 Stretch
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Check Box 열 크기 조정
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Asset 열
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Current 열
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Latest 열
    
        header.setMinimumSectionSize(20)  # 최소 크기 제한

        # 버튼 UI
        self.update_button = QPushButton("Update Selected")
        self.update_button.setEnabled(False)  
        self.update_button.clicked.connect(self.apply_selected_versions)

        self.all_latest_button = QPushButton("All to Latest")
        self.all_latest_button.clicked.connect(self.confirm_all_to_latest)

        self.select_all_button = QPushButton("Select All / Deselect All")
        self.select_all_button.clicked.connect(self.toggle_all_checkboxes)

        # 버튼 배치
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.all_latest_button)
        button_layout.addWidget(self.select_all_button)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        self.setCentralWidget(main_widget)


    # 의심군

    # 확장자를 가진 파일목록을 가져온 
    def get_usd_files(self):
        """USD 파일 목록을 가져오고 버전 정보를 추출"""
        print(f"🔍 검색 경로: {USD_DIRECTORY}")
        
        if not os.path.exists(USD_DIRECTORY):
            print(f" 경로가 존재하지 않습니다: {USD_DIRECTORY}")
            return []
            
        if not os.access(USD_DIRECTORY, os.R_OK):
            print(f" 읽기 권한이 없습니다: {USD_DIRECTORY}")
            return []
        
        try:
            usd_files = [f for f in os.listdir(USD_DIRECTORY) if f.endswith((".usd", ".mb", ".usdc"))]
            print(f"✅ 발견된 USD 파일: {len(usd_files)}개")
            for f in usd_files:
                print(f"  - {f}")
            return usd_files
        except Exception as e:
            print(f"파일 목록 조회 중 오류 발생: {str(e)}")
            return []

    def get_latest_version(self, asset_dir, asset_name):
        """디렉토리에서 특정 에셋의 최신 버전 찾기"""
        if not os.path.exists(asset_dir):
            print(f"경로 없음: {asset_dir}")
            return 1  # 기본 버전 반환
        
        asset_base, ext = os.path.splitext(asset_name)  # 파일명과 확장자 분리
        asset_base = re.sub(r"_v\d+", "", asset_base)  # 버전 번호 제거

        versions = []
        for file in os.listdir(asset_dir):
            if file.startswith(asset_base) and file.endswith(ext):  # 같은 확장자 확인
                match = re.search(r"v(\d+)", file)
                if match:
                    versions.append(int(match.group(1)))

        if versions:
            latest_version = max(versions)  # 가장 높은 숫자의 버전 반환
            print(f"🔍 최신 버전 찾음: {asset_name} → v{latest_version:03d}")
            return latest_version
        else:
            return 1  # 기본 버전


    def get_available_versions(self, asset_dir, asset_name):
        """디렉토리에서 해당 에셋의 모든 버전 목록을 가져오기"""
        if not os.path.exists(asset_dir):
            print(f" 경로 없음: {asset_dir}")
            return ["v001"]  # 기본 버전

        print(f"검색 중: {asset_dir}")

        # 정확한 파일명 패턴을 얻기 위해 파일 확장자 분리
        asset_base, ext = os.path.splitext(asset_name)
        asset_base = re.sub(r"_v\d+(?:\.\d+)?", "", asset_base)  # 버전 제거 (정확한 이름 추출)

        versions = []
        for file in os.listdir(asset_dir):
            if file.startswith(asset_base) and file.endswith(ext):  # 확장자까지 일치해야 함
                match = re.search(r"v(\d+)", file)
                if match:
                    version_number = int(match.group(1))
                    versions.append(version_number)

        versions.sort()  # 정렬
        print(f" {asset_base} - 발견된 버전 목록: {versions}")
        return [f"v{str(v).zfill(3)}" for v in versions] if versions else ["v001"]

        
    def update_table(self):
        version_data = self.get_referenced_assets()
        self.set_table_items(version_data)
        
    def get_clean_asset_name(self, asset_name):
        """파일명에서 불필요한 `{}` 기호 및 숫자를 제거"""
        asset_name = re.sub(r"\{\d+\}", "", asset_name)
        asset_name = re.sub(r"_v\d{3}", "", asset_name)  # `_v003` 같은 버전 제거
        asset_name = asset_name.replace(" ", "")
        return asset_name
    
    def get_referenced_assets(self):
        """현재 씬에서 참조된 에셋을 가져오기"""
        references = cmds.file(q=True, reference=True) or []
        asset_data = []

        for ref in references:
            asset_name = os.path.basename(ref)  # 파일 이름 추출
            clean_asset_name = self.get_clean_asset_name(asset_name)
            clean_asset_name = re.sub(r"_v\d{3}", "", clean_asset_name)  # v### 패턴 제거

            match = re.search(r"v(\d+)", asset_name)  # 파일명에서 버전 찾기
            current_version = int(match.group(1)) if match else 1

            # 최신 버전 확인
            latest_version = self.get_latest_version(USD_DIRECTORY, clean_asset_name)

            asset_data.append((clean_asset_name, current_version, latest_version))  # 🚀 변경됨!

        return asset_data
    
    def get_latest_version(self, asset_dir, asset_name):
        """디렉토리 내에서 최신 버전을 찾기"""
        if not os.path.exists(asset_dir):
            print(f" 경로 없음: {asset_dir}")
            return 1  # 기본 버전-return
        asset_base, ext = os.path.splitext(asset_name)
        asset_base = re.sub(r"_v\d+", "", asset_base)  # 버전 번호 제거

        versions = []
        for file in os.listdir(asset_dir):  # ✅ asset_dir에서 파일 검색
            if file.startswith(asset_base) and file.endswith(ext):
                match = re.search(r"v(\d+)", file)
                if match:
                    versions.append(int(match.group(1)))

        return max(versions) if versions else 1

    def set_table_items(self, version_data):
        """테이블 항목 설정"""
        self.table.setRowCount(len(version_data))

        for row, (asset_name, current_version, latest_version) in enumerate(version_data):
            asset_dir = USD_DIRECTORY
            print ("최신버전 검색: {asset_name} in {asset_dir}")

            latest_version = self.get_latest_version(USD_DIRECTORY, asset_name)

            latest_status = "🟢" if f"v{latest_version:03d}" == f"v{current_version:03d}" else "🟡"
            latest_item = QTableWidgetItem(f"{latest_status} v{latest_version:03d}")
            latest_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 3, latest_item)
            asset_item = QTableWidgetItem(asset_name)  
            asset_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, asset_item)


            # 체크박스 추가
            check_widget = QWidget()
            check_layout = QHBoxLayout()
            check_layout.setAlignment(Qt.AlignCenter)
            check_layout.setContentsMargins(0, 0, 0, 0)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_checkbox_state)  # 체크박스 상태 변경 감지
            checkbox.setText("✔")
            checkbox.setStyleSheet(
               "QCheckBox {"
               "    color: red;"
               "}"   
                "QCheckBox::indicator {"
                "    width: 15px;"
                "    height: 15px;"
                "   border: 0.5px solid white;"  # 흰색 테두리 추가
                "   background-color: white;" 
                "}"
                "QCheckBox::indicator:checked {"
                "   background-color: red;"
                "   border: 2px solid red;"
                "}"
            )

            checkbox.setFixedSize(15, 15)
            check_layout.addWidget(checkbox)
            check_widget.setLayout(check_layout)
            self.table.setCellWidget(row, 0, check_widget)

            # 에셋 이름 추가
            asset_item = QTableWidgetItem(asset_name)
            asset_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, asset_item)

            # 현재 버전 추가 (콤보박스 수정)
            combo = QComboBox()
            asset_dir = USD_DIRECTORY  # 고정된 경로 사용
            available_versions = self.get_available_versions(asset_dir, asset_name)
            combo.addItems(available_versions)
            combo.setCurrentText(f"v{current_version:03d}")  # 현재 버전 설정
            combo.currentIndexChanged.connect(lambda _, r=row, c=combo: self.update_maya_reference(r, c))  # 🚀 연결!
            self.table.setCellWidget(row, 2, combo)

            # 최신 버전 상태 업데이트
            latest_status = "🟢" if f"v{latest_version:03d}" == f"v{current_version:03d}" else "🟡"
            latest_item = QTableWidgetItem(f"{latest_status} v{latest_version:03d}")
            latest_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, latest_item)

            # 클릭기능
            self.table.cellClicked.connect(self.onCellClicked)

    def update_table(self):
        """Maya에서 에셋 버전 정보 가져와 테이블 업데이트"""
        version_data = self.get_referenced_assets()
        self.set_table_items(version_data)

    def update_checkbox_state(self):
        """체크박스 상태 변경 시 Update Selected 버튼 활성화"""
        checked = any(
            self.table.cellWidget(row, 0).layout().itemAt(0).widget().isChecked()
            for row in range(self.table.rowCount())
        )
        self.update_button.setEnabled(checked)

    def apply_selected_versions(self):
        """선택된 항목을 최신 버전으로 업데이트"""
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                combo = self.table.cellWidget(row, 2)
                latest_item = self.table.item(row, 3)
                latest_version = latest_item.text().split(" ")[-1]
                combo.setCurrentText(latest_version)
    def confirm_all_to_latest(self):
        """모든 항목을 최신 버전으로 업데이트 전 확인 메시지"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Confirm Update")
        msg_box.setText("Are you sure you want to update all assets to the latest version?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if msg_box.exec() == QMessageBox.Yes:
            for row in range(self.table.rowCount()):
                combo = self.table.cellWidget(row, 2)
                latest_item = self.table.item(row, 3)
                latest_version = latest_item.text().split(" ")[-1]
                combo.setCurrentText(latest_version)
                self.update_version_status(row, combo, latest_item)
    

    def toggle_all_checkboxes(self):
        """모든 체크박스를 선택/해제하는 기능"""
        new_state = Qt.Unchecked if any(
            self.table.cellWidget(i, 0).layout().itemAt(0).widget().isChecked()
            for i in range(self.table.rowCount())
        ) else Qt.Checked

        for i in range(self.table.rowCount()):
            self.table.cellWidget(i, 0).layout().itemAt(0).widget().setChecked(new_state)
    # def update_version_status(self, row, combo, latest_item):
    #     """버전 변경 후 UI 갱신"""
    #     asset_name = self.table.item(row, 1).text()  # 에셋 이름
    #     asset_dir = USD_DIRECTORY  # 고정된 디렉토리
        
    #     # 최신 버전 다시 가져오기
    #     latest_version = self.get_latest_version(asset_dir, asset_name)
    #     current_version = int(combo.currentText().replace("v", ""))  # 현재 선택된 버전 가져오기

    #     # 🟢(최신) 또는 🟡(구버전) 상태 업데이트
    #     latest_status = "🟢" if current_version == latest_version else "🟡"
    #     latest_item.setText(f"{latest_status} v{latest_version:03d}")

    #     print(f"✅ UI 업데이트: {asset_name} | 현재: v{current_version:03d} | 최신: v{latest_version:03d}")

    def update_version_status(self, row, combo, latest_item):
        """최신 버전 상태 UI 업데이트"""
        asset_name = self.table.item(row, 1).text()  # 에셋 이름
        asset_dir = USD_DIRECTORY  # 고정된 디렉토리
        
        # 최신 버전 다시 가져오기
        latest_version = self.get_latest_version(asset_dir, asset_name)
        current_version = int(combo.currentText().replace("v", ""))  # 현재 선택된 버전 가져오기

        # 최신 상태 반영 (🟢 최신 / 🟡 구버전)
        latest_status = "🟢" if current_version == latest_version else "🟡"
        latest_item.setText(f"{latest_status} v{latest_version:03d}")

        print(f"UI 업데이트: {asset_name} | 현재: v{current_version:03d} | 최신: v{latest_version:03d}")

    def onCellClicked(self, row, column):
        """✅ 테이블에서 Asset 클릭 시 Maya에서 해당 오브젝트 선택"""
        if column == 1:  # 🔹 Asset 열(파일명) 클릭 시
            self.selectAssetInMaya(row)


    def selectAssetInMaya(self, row):
        """✅ 선택한 테이블 행의 에셋을 Maya에서 선택"""
        asset_name = self.table.item(row, 1).text()  # 에셋 이름 가져오기 (예: "ground.mb")
        clean_asset_name = self.get_clean_asset_name(asset_name) 

        # 🔍 Maya에서 해당 에셋과 연결된 참조 찾기
        refs = cmds.file(q=True, reference=True) or []
        ref_nodes = []
        
        for ref in refs:
            abs_ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            ref_base = os.path.basename(abs_ref_path)
            clean_ref_name = self.get_clean_asset_name(ref_base)

            print(f"참조 파일 검사중: {abs_ref_path} → 정리된 이름: {clean_ref_name}")

            if clean_asset_name == clean_ref_name:  # 참조 파일명과 검사한 파일명이 같은 경우
                try:
                    ref_node = cmds.referenceQuery(ref, referenceNode=True)
                    ref_nodes.append(ref_node)
                    print (f"참조 파일 찾음 : {ref_node}")
                except RuntimeError:
                    print (f"{asset_name} 참조 파일을 찾을 수 없음")            

        if not ref_nodes:
            print(f"⚠️ '{asset_name}'의 참조를 찾을 수 없습니다.")
            return

        # 🔄 Maya 오브젝트 찾기
        object_list = []
        for ref_node in ref_nodes:
            try: 
                objects = cmds.referenceQuery(ref_node, nodes=True ,dagPath=True) or []
                object_list.extend(objects)
            except RuntimeError:
                print (f"{ref_node}에서 참조 파일을 찾을 수 없음")

        if object_list:
            cmds.select(clear=True)
            cmds.select(object_list, replace=True)
            print(f"✅ '{asset_name}' 선택 완료: {object_list}")
        else:
            print(f"⚠️ '{asset_name}'에 연결된 오브젝트가 없습니다.")


    def update_maya_reference(self, row, combo):
        """ Maya에서 참조된 파일을 새로운 버전으로 업데이트 """
        new_version = combo.currentText().replace("v", "")   # 사용자가 선택한 새 버전 (예: "v003")
        asset_name = self.table.item(row, 1).text()  # 에셋 이름 가져오기 (예: "object.mb")
        
        #  올바른 버전 파일명 생성
        base_name, ext = os.path.splitext(asset_name)
        base_name = re.sub(r"_v\d{3}", "", base_name)  # 기존 "_v###" 패턴 제거


        new_file = f"{base_name}_v{new_version}{ext}"  # 예: "object_v003.mb"
        new_path = os.path.normpath(os.path.join(USD_DIRECTORY, new_file)) #경로 정리 (운영체제 호환)

        print(f"변경할 참조 파일: {new_path}")  # 경로 확인용 로그
        # 1. 디렉토리 내 모든 파일 검색하여 참조 가능 여부 확인
        matching_files = []
        for root, _, files in os.walk(USD_DIRECTORY):  # 디렉토리 내 모든 파일 검색
            for file in files:
                if file.startswith(base_name) and file.endswith(ext):  # 같은 확장자 & 같은 기본 이름
                    matching_files.append(os.path.join(root, file))

        if not matching_files:
            print(f"오류: {base_name} 관련 파일이 디렉토리에 존재하지 않음!")
            return

        print(f"발견된 파일 목록: {matching_files}")  # 찾은 파일 목록 출력

        # 2. Maya에서 현재 참조된 파일 찾기
        refs = cmds.file(q=True, reference=True) or []
        ref_node = None
        ref_path = None

        for ref in refs:
            # abs_ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            abs_ref_path = cmds.referenceQuery(ref, filename=True)
            print(f" 참조 파일 검사중: {abs_ref_path}")

            if asset_name in ref or any(f in abs_ref_path for f in matching_files):  # 기존 참조 확인
                try:
                    ref_node = cmds.referenceQuery(ref, referenceNode=True)
                    ref_path = abs_ref_path
                    print(f"참조 파일 찾음! {ref_node} → {ref_path}")
                    break
                except RuntimeError:
                    print(f"⚠️ 오류: 참조 파일을 찾을 수 없음! {ref}")

        # 3. 새 버전이 있는지 확인 후 적용
        if not os.path.exists(new_path):
            print(f" 오류: 새 버전 파일이 존재하지 않음! ({new_path})")
            return

        # 기존 참조를 강제로 언로드하고 새 경로로 변경
        if ref_node:
            try:
                print(f" 참조 변경 중: {ref_node} → {new_path}")
                cmds.file(unloadReference=ref_node)  # 기존 참조 언로드
                cmds.file(new_path, loadReference=ref_node, force=True)  # 새로운 파일 로드
                print(f" {asset_name} → {new_file} 업데이트 완료")

                latest_item = self.table.item(row, 3)
                self.update_version_status(row, combo, latest_item)

                self.update_table()

            except Exception as e:
                print(f"⚠️ 업데이트 실패: {str(e)}")
        else:
            print(f"참조 노드를 찾을 수 없음. {asset_name}의 참조를 확인하세요.")
    


def launch_ui():
    """Maya에서 UI 실행"""
    global window
    try:
        window.close()
    except:
        pass

    window = VersionCheckUI()
    window.show()


if not cmds.about(batch=True):
    cmds.evalDeferred(launch_ui)

