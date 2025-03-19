
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
from maya_asset_manager import AssetManager




class MayaReferenceManager:
    """🎯 Maya 내 참조 및 오브젝트 선택 기능 관리"""

    @staticmethod
    def select_asset_by_name(asset_name):
        """Maya 내에서 해당 에셋을 선택"""
        references = cmds.file(q=True, reference=True) or []

        for ref in references:
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            if asset_name in ref_path:
                ref_node = cmds.referenceQuery(ref, referenceNode=True)
                objects_to_select = cmds.referenceQuery(ref_node, nodes=True, dagPath=True) or []
                if objects_to_select:
                    cmds.select(objects_to_select, replace=True)
                    print(f"✅ '{asset_name}' 선택 완료: {objects_to_select}")
                    return

    @staticmethod
    def get_referenced_assets():
        """현재 씬에서 참조된 에셋을 가져오기 (파일 경로에서 정확한 버전 가져오기)"""
        references = cmds.file(q=True, reference=True) or []
        asset_data = []

        for ref in references:
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
            asset_name = AssetManager.get_clean_asset_name(ref_path)  #  경로 기반 에셋 이름 추출

            #  현재 버전 정확히 추출 (scene.v002.ma 같은 파일명에서 v002 추출)
            current_version_match = re.search(r"\.v(\d{3})", os.path.basename(ref_path))
            current_version = current_version_match.group(1) if current_version_match else "v001"
    
            #  최신 버전 찾기
            latest_version = AssetManager.get_latest_version(asset_name)

            asset_data.append((asset_name, current_version, latest_version)) 
        return asset_data
    
    @staticmethod
    def refresh_maya_reference(self):
        references = cmds.file(q=True, reference=True) or []
        for ref in references:
            try:
                ref_node = cmds.referenceQuery(ref, referenceNode=True)
                cmds.file(unloadReference=ref_node)  # 참조 파일 언로드
                cmds.file(ref, loadReference=ref_node, force=True)  # 최신 버전으로 참조 파일 로드
                print(f"✅ 참조 업데이트 완료: {ref}")
            except Exception as e:
                print(f"⚠️ 참조 업데이트 실패: {e}")

    @staticmethod
    def select_asset(row):
        """Maya에서 특정 에셋을 선택 (UI 접근 없이 디렉토리 기반 검색)"""
        
        #  현재 씬에서 참조된 파일 목록 가져오기
        references = cmds.file(q=True, reference=True) or []
        if not references:
            print("⚠️ 현재 씬에 참조된 파일이 없습니다.")
            return

        # 참조된 파일에서 row에 해당하는 파일 찾기
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

        print(f"선택된 에셋: {clean_asset_name} (경로: {selected_path})")

        # 3️Maya에서 해당 참조를 기반으로 객체 찾기
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

        # 4️오브젝트 찾고 선택
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
            print(f" '{asset_name}' 선택 완료: {object_list}")
        else:
            print(f"⚠️ '{asset_name}'에 연결된 오브젝트가 없습니다.")
