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


ASSET_DIRECTORY = "/nas/spirit/spirit/sequences/SQ001/SH0010/MMV/work/maya"


custom_script_path = "/home/rapa/NA_Spirit/maya/"

if custom_script_path not in sys.path:
    sys.path.append(custom_script_path)


class VersionCheckUI(QMainWindow):
    asset_paths_dict = {} 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASSET & Maya Version Matching Check")
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

        self.select_all_button = QPushButton("Select All / Deselect All")
        self.select_all_button.clicked.connect(self.toggle_all_checkboxes)

        # 버튼 배치
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.select_all_button)

        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        self.setCentralWidget(main_widget)
    def get_current_version(self, row):
        """현재 선택된 버전을 가져오는 메서드"""
        combo = self.table.cellWidget(row, 2)
        return combo.currentText() if combo else None

    def get_latest_version(self, row):
        """테이블에서 최신 버전 정보를 가져오는 메서드"""
        latest_item = self.table.item(row, 3)
        return latest_item.text().split(" ")[-1] if latest_item else None

    def update_table(self):
        version_data = MayaReferenceManager.get_referenced_assets()
        self.set_table_items(version_data)

    def set_table_items(self, version_data):
        """테이블 항목 설정"""
        self.table.setRowCount(len(version_data))

        for row, (asset_name, current_version, latest_version) in enumerate(version_data):
            asset_dir = AssetManager.get_asset_directory(asset_name)
            latest_version = AssetManager.get_latest_version(asset_name)

            # 🚀 current_version과 latest_version이 None이 아니고 문자열인지 확인
            if not isinstance(current_version, str):
                current_version = str(current_version) if current_version is not None else "v001"
            if not isinstance(latest_version, str):
                latest_version = str(latest_version) if latest_version is not None else "v001"

                # 🚀 문자열인 current_version과 latest_version을 정수로 변환
            try:
                current_version_int = int(re.sub(r"\D", "", current_version))  # v### → ###
                latest_version_int = int(re.sub(r"\D", "", latest_version))  # v### → ###
            except ValueError:
                print(f"⚠️ 버전 변환 오류: {current_version}, {latest_version}")
                current_version_int, latest_version_int = 1, 1  # 기본값 설정

            latest_status = "🟢" if current_version_int == latest_version_int else "🟡"
            latest_item = QTableWidgetItem(f"{latest_status} v{latest_version_int:03d}")
            latest_item.setTextAlignment(Qt.AlignCenter)
            latest_item.setFlags(Qt.ItemIsEnabled)  # 클릭 비활성화 

            # Asset 이름 
            asset_item = QTableWidgetItem(asset_name)  
            asset_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, asset_item)

            # Current 버전(콤보박스)
            combo = QComboBox()
            available_versions = AssetManager.get_available_versions(asset_name)
            combo.addItems(available_versions)
            combo.wheelEvent = lambda event: None  # 마우스 휠 비활성화


            combo.setCurrentText(f".v{current_version_int:03d}")    # 현재 버전 설정
            combo.currentIndexChanged.connect(lambda _, r=row, c=combo: self.confirm_version_change(r, c))
            self.table.setCellWidget(row, 2, combo)


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

            # 🚀 최신 버전 상태 업데이트 (정수 비교 방식으로 수정)
            latest_status = "🟢" if latest_version_int == current_version_int else "🟡"

            # 🚀 최신 버전 정보 텍스트 업데이트
            latest_item = QTableWidgetItem(f"{latest_status} v{latest_version_int:03d}")
            latest_item.setTextAlignment(Qt.AlignCenter)
            latest_item.setFlags(Qt.ItemIsEnabled)  # 클릭 비활성화
            self.table.setItem(row, 3, latest_item)

            # 클릭기능
            self.table.cellClicked.connect(self.onCellClicked)


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
                    combo.setCurrentText(str(latest_version))

    def is_ui_valid(ui_instance):
        return ui_instance is not None and ui_instance.table is not None

    def is_asset_valid(asset_item):
        return asset_item is not None


    def toggle_all_checkboxes(self):
        """모든 체크박스를 선택/해제하는 기능"""
        new_state = Qt.Unchecked if any(
            self.table.cellWidget(i, 0).layout().itemAt(0).widget().isChecked()
            for i in range(self.table.rowCount())
        ) else Qt.Checked

        for i in range(self.table.rowCount()):
            self.table.cellWidget(i, 0).layout().itemAt(0).widget().setChecked(new_state)

    def update_version_status(self, row, combo, latest_item):
        """최신 버전 상태 UI 업데이트"""
        asset_name = self.table.item(row, 1).text()  # 에셋 이름 # 테이블 아이템을 참조하는 것은 오류가 나기 쉬움 디렉토리에서 정보가져오기  
        asset_dir = ASSET_DIRECTORY  # 고정된 디렉토리
        
        # 최신 버전 다시 가져오기
        latest_version = AssetManager.get_latest_version(asset_name)
        current_version = int(combo.currentText().replace("v", ""))  # 현재 선택된 버전 가져오기

        # 최신 상태 반영 (🟢 최신 / 🟡 구버전)
        latest_status = "🟢" if current_version == latest_version else "🟡"
        latest_item.setText(f"{latest_status} v{latest_version:03d}")

        print(f"UI 업데이트: {asset_name} | 현재: v{current_version:03d} | 최신: v{latest_version:03d}")

    def confirm_version_change(self, row, combo):
        """버전 변경 시 메시지 박스를 UI 클래스에서 처리"""
        new_version = combo.currentText()
        current_version = self.get_current_version(row)

        msg = QMessageBox.warning(
            self, "Confirm Change",
            f"Change version to {new_version}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if msg == QMessageBox.No:
            combo.blockSignals(True)
            combo.setCurrentText(current_version)
            combo.blockSignals(False)


    def onCellClicked(self, row, column):
            """ 테이블에서 Asset 클릭 시 Maya에서 해당 오브젝트 선택"""
            if column == 1:  # 🔹 Asset 열(파일명) 클릭 시
                MayaReferenceManager.select_asset(self, row)


    # def update_maya_reference(self, row, combo):
    #     """Maya에서 참조된 파일을 새로운 버전으로 업데이트"""
    #     asset_name = self.table.item(row, 1).text()
    #     new_version = combo.currentText().replace("v", "")
        
    #     base_name, ext = os.path.splitext(asset_name)
    #     base_name = re.sub(r".v\d{3}", "", base_name)

    #     new_file = f"{base_name}.v{new_version}{ext}"
    #     new_path = os.path.join(ASSET_DIRECTORY, new_file)

    #     refs = cmds.file(q=True, reference=True) or []
    #     for ref in refs:
    #         ref_node = cmds.referenceQuery(ref, referenceNode=True)
    #         ref_path = cmds.referenceQuery(ref, filename=True)

    #         if asset_name in ref_path:
    #             if not os.path.exists(new_path):
    #                 print(f"⚠️ 새 버전 파일이 존재하지 않습니다: {new_path}")
    #                 return

    #             try:
    #                 cmds.file(unloadReference=ref_node)
    #                 cmds.file(new_path, loadReference=ref_node, force=True)
    #                 print(f"✅ 참조 업데이트 완료: {asset_name} → {new_file}")

    #                 latest_item = self.table.item(row, 3)
    #                 self.update_version_status(row, combo, latest_item)

    #             except Exception as e:
    #                 print(f"⚠️ 업데이트 실패: {e}")
    # def onCellClicked(self, row, column):
    #     """✅ 테이블에서 Asset 열 클릭 시 Maya에서 해당 에셋 선택"""
    #     if column == 1:  # 🔹 Asset 열 클릭
    #         asset_name = self.table.item(row, 1).text()  # 선택된 에셋 이름 가져오기
    #         MayaReferenceManager.select_asset_by_name(asset_name)
import os
import re
import maya.cmds as cmds

def update_maya_reference(self, row, combo):
    """Maya에서 참조된 파일을 새로운 버전으로 업데이트 (디렉토리 순회 방식)"""
    
    # 🔹 현재 참조된 파일 경로 가져오기
    ref_path = cmds.referenceQuery(cmds.file(q=True, reference=True)[row], filename=True, withoutCopyNumber=True)
    
    if not ref_path or not os.path.exists(ref_path):
        print(f"⚠️ 참조 경로를 찾을 수 없습니다: {ref_path}")
        return

    # 🔹 참조된 파일이 존재하는 디렉토리 가져오기
    asset_dir = os.path.dirname(ref_path)
    
    # 🔹 파일 이름에서 버전 정보 제거
    base_name, ext = os.path.splitext(os.path.basename(ref_path))
    base_name_no_version = re.sub(r"\.v\d{3}", "", base_name)  # `v001` 같은 버전 제거

    # 🔹 해당 디렉토리 내에서 최신 버전 찾기
    latest_version = 0
    latest_file = None

    for file in os.listdir(asset_dir):
        if file.startswith(base_name_no_version) and file.endswith(ext):
            match = re.search(r"\.v(\d{3})", file)
            if match:
                version = int(match.group(1))
                if version > latest_version:
                    latest_version = version
                    latest_file = file

    if not latest_file:
        print(f"⚠️ 최신 버전을 찾을 수 없습니다: {base_name_no_version}")
        return

    latest_path = os.path.join(asset_dir, latest_file)

    # 🔹 Maya 참조 업데이트
    try:
        ref_node = cmds.referenceQuery(ref_path, referenceNode=True)
        cmds.file(unloadReference=ref_node)
        cmds.file(latest_path, loadReference=ref_node, force=True)
        print(f"✅ 참조 업데이트 완료: {ref_path} → {latest_file}")

        # 🔹 UI 최신 상태 업데이트
        latest_item = self.table.item(row, 3)
        self.update_version_status(row, combo, latest_item)

    except Exception as e:
        print(f"⚠️ 업데이트 실패: {e}")



class AssetManager:
    """🚀 파일 및 버전 정보를 관리하는 클래스"""

    ASSET_DIRECTORY =  "/home/rapa/NA_Spirit/maya/"


    @staticmethod
    def update_asset_info():
        """🔹 현재 씬에서 참조된 에셋 정보를 JSON에 저장"""
        references = cmds.file(q=True, reference=True) or []
        asset_data = {}

        for ref in references:
            asset_name = os.path.basename(ref)  # 파일명 추출
            clean_asset_name = AssetManager.get_clean_asset_name(asset_name)
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            ref_node = cmds.referenceQuery(ref, referenceNode=True)
            object_list = cmds.referenceQuery(ref_node, nodes=True, dagPath=True) or []

            asset_data[clean_asset_name] = {
                "path": ref_path,
                "objects": object_list
            }



    # @staticmethod
    # def get_clean_asset_name(asset_path):
    #     """✅ 파일 경로에서 Prop/ 다음에 오는 폴더명을 에셋 이름으로 가져오기"""
    #     match = re.search(r"/Prop/([^/]+)/RIG/", asset_path)
    #     if match:
    #         return match.group(1)  # `Prop/` 다음의 폴더명(에셋 이름) 반환
        
    #     return "unknown"  # 경로가 예상과 다르면 기본값 반환

    @staticmethod
    def get_clean_asset_name(asset_path):
        """✅ 파일 경로에서 'Prop/' 다음에 오는 폴더명을 에셋 이름으로 가져오기"""
        match = re.search(r"/Prop/([^/]+)/RIG/", asset_path)
        if match:
            return match.group(1)  # `Prop/` 다음 폴더명(에셋 이름) 반환
        
        return "unknown"  # 경로가 예상과 다르면 기본값 반환


   
    @staticmethod
    def get_latest_version(asset_name):
        """최신 버전 찾기"""
        versions = []
        for file in os.listdir(ASSET_DIRECTORY):
            if file.startswith(asset_name) and file.endswith(".mb"):
                match = re.search(r"\.v(\d{3})\.mb", file)
                if match:
                    versions.append(int(match.group(1)))

        return f".v{max(versions):03d}" if versions else ".v001"

    @staticmethod
    def get_asset_directory(asset_name):
        """해당 에셋이 존재하는 디렉토리 경로 가져오기"""
        refs = cmds.file(q=True, reference=True) or []
        for ref in refs:
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            if asset_name in ref_path:
                return os.path.dirname(ref_path)  # 참조된 파일의 경로 반환

        return None
        

    

    @staticmethod
    def get_available_versions(asset_name):
        """특정 에셋의 모든 버전 가져오기"""
        versions = []
        for file in os.listdir(ASSET_DIRECTORY):
            if file.startswith(asset_name) and file.endswith(".mb"):
                match = re.search(r"\.v(\d{3})\.mb", file)
                if match:
                    versions.append(int(match.group(1)))

        return [f".v{str(v).zfill(3)}" for v in sorted(versions)] if versions else [".v001"]
    @staticmethod
    def update_asset_info():
        """🔹 현재 씬에서 참조된 에셋 정보를 JSON에 저장"""
        references = cmds.file(q=True, reference=True) or []
        asset_data = {}

        for ref in references:
            asset_name = os.path.basename(ref)  # 파일명 추출
            clean_asset_name = AssetManager.get_clean_asset_name(asset_name)
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            ref_node = cmds.referenceQuery(ref, referenceNode=True)
            object_list = cmds.referenceQuery(ref_node, nodes=True, dagPath=True) or []

            asset_data[clean_asset_name] = {
                "path": ref_path,
                "objects": object_list
            }

        return asset_data



class MayaReferenceManager:
    """🎯 Maya 내 참조 및 오브젝트 선택 기능 관리"""
    @staticmethod
    def select_asset_by_name(asset_name):
        """🔹 JSON 데이터를 기반으로 에셋을 선택"""
        asset_dict = {}
        if asset_name not in asset_dict:
            print(f"⚠️ '{asset_name}' 에셋을 찾을 수 없습니다.")
            return

        objects_to_select = asset_dict[asset_name]["objects"]

        if objects_to_select:
            cmds.select(clear=True)
            cmds.select(objects_to_select, replace=True)
            print(f"✅ '{asset_name}' 선택 완료: {objects_to_select}")
        else:
            print(f"⚠️ '{asset_name}'에 연결된 오브젝트가 없습니다.")


    @staticmethod
    def get_referenced_assets():
        """✅ 현재 씬에서 참조된 에셋을 가져오기 (파일 경로에서 에셋명 추출)"""
        references = cmds.file(q=True, reference=True) or []
        asset_data = []

        for ref in references:
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            asset_name = AssetManager.get_clean_asset_name(ref_path)  # ✅ 경로 기반 에셋 이름 추출

            # 🔹 현재 버전 추출 (파일명에서 버전 번호 가져오기)
            current_version_match = re.search(r"\.v(\d{3})", os.path.basename(ref_path))
            current_version = f"v{int(current_version_match.group(1)):03d}" if current_version_match else "v001"

            # 🔹 최신 버전 찾기
            latest_version = AssetManager.get_latest_version(asset_name)

            asset_data.append((asset_name, current_version, latest_version))  # ✅ (3개 값) 반환

        return asset_data


    @staticmethod
    def select_asset(row):
        """✅ Maya에서 특정 에셋을 선택 (UI 접근 없이 디렉토리 기반 검색)"""
        
        # 1️⃣ 현재 씬에서 참조된 파일 목록 가져오기
        references = cmds.file(q=True, reference=True) or []
        if not references:
            print("⚠️ 현재 씬에 참조된 파일이 없습니다.")
            return

        # 2️⃣ 참조된 파일에서 row에 해당하는 파일 찾기
        asset_paths = []
        for ref in references:
            try:
                ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
                asset_paths.append(ref_path)
            except RuntimeError:
                print(f"⚠️ 참조 파일 정보를 가져올 수 없습니다: {ref}")

        if row >= len(asset_paths):
            print(f"⚠️ {row}번째 행에 해당하는 참조 파일을 찾을 수 없습니다.")
            return

        selected_path = asset_paths[row]
        asset_name = os.path.basename(selected_path)  # 파일명 추출
        asset_dir = os.path.dirname(selected_path)   # 디렉토리 경로 추출
        clean_asset_name = AssetManager.get_clean_asset_name(asset_name)

        print(f"🔍 선택된 에셋: {clean_asset_name} (경로: {selected_path})")

        # 3️⃣ Maya에서 해당 참조를 기반으로 객체 찾기
        ref_nodes = []
        for ref in references:
            try:
                ref_node = cmds.referenceQuery(ref, referenceNode=True)
                ref_nodes.append(ref_node)
            except RuntimeError:
                print(f"⚠️ {asset_name} 참조 노드를 찾을 수 없음.")

        if not ref_nodes:
            print(f"⚠️ '{asset_name}'의 참조를 찾을 수 없습니다.")
            return

        # 4️⃣ 오브젝트 찾고 선택
        object_list = []
        for ref_node in ref_nodes:
            try:
                objects = cmds.referenceQuery(ref_node, nodes=True, dagPath=True) or []
                object_list.extend(objects)
            except RuntimeError:
                print(f"⚠️ '{ref_node}'에서 참조된 오브젝트를 찾을 수 없음.")

        if object_list:
            cmds.select(clear=True)
            cmds.select(object_list, replace=True)
            print(f"✅ '{asset_name}' 선택 완료: {object_list}")
        else:
            print(f"⚠️ '{asset_name}'에 연결된 오브젝트가 없습니다.")


    @staticmethod
    def update_reference(asset_name, new_version):
        """✅ Maya에서 참조된 파일을 새로운 버전으로 업데이트"""
        pass


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
