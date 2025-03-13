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


class AssetManager(QMainWindow):
    """🚀 파일 및 버전 정보를 관리하는 클래스"""
    ASSET_DIRECTORY = "/nas/spirit/spirit/assets/Prop"

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
        asset_dir = AssetManager.get_asset_directory(asset_name)
        if not asset_dir or not os.path.exists(asset_dir):
            print(f"⚠️ '{asset_name}'의 디렉토리를 찾을 수 없음.")
            return "v001"  # 기본값 v001 반환

        versions = []
        for file in os.listdir(asset_dir):
            match = re.search(r"\.v(\d{3})\.mb", file)
            if match:
                versions.append(int(match.group(1)))
        
        print(f"Versions found: {versions}")  # 디버깅 출력
        
        if versions:
            latest_version = max(versions)  # 가장 큰 버전 번호 선택
            return f"v{latest_version:03d}"
        else:
            return "v001"  # 최신 버전이 없으면 v001 반환
        


    @staticmethod
    def get_asset_directory(asset_name):
        """해당 에셋이 존재하는 디렉토리 경로 가져오기"""
        asset_path = os.path.join(ASSET_DIRECTORY, asset_name, "RIG", "publish", "maya")
        
        if os.path.exists(asset_path):
            return asset_path
        return None
    
    @staticmethod
    def get_asset_paths():
        """디렉토리 내 모든 에셋 경로를 딕셔너리로 반환"""
        asset_paths = {}
        asset_dirs = os.listdir(ASSET_DIRECTORY)  # ASSET_DIRECTORY에서 모든 파일 리스트 가져오기

        for asset_name in asset_dirs:
            asset_paths[asset_name] = AssetManager.get_asset_directory(asset_name)

        return asset_paths


    @staticmethod
    def get_all_asset_versions():
        """디렉토리 내 모든 에셋과 그에 해당하는 버전들을 딕셔너리로 반환"""
        asset_versions = {}
        asset_dirs = os.listdir(ASSET_DIRECTORY)  # ASSET_DIRECTORY에서 모든 파일 리스트 가져오기

        for asset_name in asset_dirs:
            asset_versions[asset_name] = AssetManager.get_available_versions(asset_name)

        return asset_versions
    

    @staticmethod
    def get_available_versions(asset_name):
        """특정 에셋의 모든 버전 가져오기"""
        asset_dir = AssetManager.get_asset_directory(asset_name)
        if not asset_dir or not os.path.exists(asset_dir):
            print(f"⚠️ '{asset_name}'의 디렉토리를 찾을 수 없음.")
            return "v001"  # 기본값 v001 반환

        versions = []
        for file in os.listdir(asset_dir):
            match = re.search(r"\.v(\d{3})\.(ma|mb)", file)
            if match:
                versions.append(int(match.group(1)))
        
        print(f"Versions found: {versions}")  # 디버깅 출력  
        return [f".v{v:03d}" for v in versions] if versions else [".v001"]


    @staticmethod
    def get_referenced_asset_paths():
        """현재 씬에서 참조된 에셋들의 경로를 딕셔너리 형태로 반환"""
        references = cmds.file(q=True, reference=True) or []
        asset_paths = {}

        for ref in references:
            asset_name = os.path.basename(ref)  # 파일명 추출
            clean_asset_name = AssetManager.get_clean_asset_name(asset_name)
            ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)

            # 에셋 경로를 딕셔너리에 저장
            asset_paths[clean_asset_name] = ref_path

        return asset_paths


# class AssetManager:
#     """파일 및 버전 정보를 관리하는 클래스"""
#     ASSET_DIRECTORY = "/nas/spirit/spirit/assets/Prop"

#     @staticmethod
#     def update_asset_info():
#         """🔹 현재 씬에서 참조된 에셋 정보를 JSON에 저장"""
#         references = cmds.file(q=True, reference=True) or []
#         asset_data = {}

#         for ref in references:
#             asset_name = os.path.basename(ref)  # 파일명 추출
#             clean_asset_name = AssetManager.get_clean_asset_name(asset_name)
#             ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
#             ref_node = cmds.referenceQuery(ref, referenceNode=True)
#             object_list = cmds.referenceQuery(ref_node, nodes=True, dagPath=True) or []

#             asset_data[clean_asset_name] = {
#                 "path": ref_path,
#                 "objects": object_list
#             }

#     @staticmethod
#     def get_clean_asset_name(asset_path):
#         """✅ 파일 경로에서 'Prop/' 다음에 오는 폴더명을 에셋 이름으로 가져오기"""
#         match = re.search(r"/Prop/([^/]+)/RIG/", asset_path)
#         if match:
#             return match.group(1)  # `Prop/` 다음 폴더명(에셋 이름) 반환
        
#         return "unknown"  # 경로가 예상과 다르면 기본값 반환

#     @staticmethod
#     def get_latest_version(asset_name):
#         """최신 버전 찾기"""
#         asset_dir = AssetManager.get_asset_directory(asset_name)
#         if not asset_dir or not os.path.exists(asset_dir):
#             print(f"⚠️ '{asset_name}'의 디렉토리를 찾을 수 없음.")
#             return "v001"  # 기본값 v001 반환

#         versions = []
#         for file in os.listdir(asset_dir):
#             match = re.search(r"\.v(\d{3})\.mb", file)
#             if match:
#                 versions.append(int(match.group(1)))
        
#         print(f"Versions found: {versions}")  # 디버깅 출력
        
#         if versions:
#             latest_version = max(versions)  # 가장 큰 버전 번호 선택
#             return f"v{latest_version:03d}"
#         else:
#             return "v001"  # 최신 버전이 없으면 v001 반환
        


#     @staticmethod
#     def get_asset_directory(asset_name):
#         """해당 에셋이 존재하는 디렉토리 경로 가져오기"""
#         asset_path = os.path.join(ASSET_DIRECTORY, asset_name, "RIG", "publish", "maya")
        
#         if os.path.exists(asset_path):
#             return asset_path
#         return None
    
#     @staticmethod
#     def get_asset_paths():
#         """디렉토리 내 모든 에셋 경로를 딕셔너리로 반환"""
#         asset_paths = {}
#         asset_dirs = os.listdir(ASSET_DIRECTORY)  # ASSET_DIRECTORY에서 모든 파일 리스트 가져오기

#         for asset_name in asset_dirs:
#             asset_paths[asset_name] = AssetManager.get_asset_directory(asset_name)

#         return asset_paths


#     @staticmethod
#     def get_all_asset_versions():
#         """디렉토리 내 모든 에셋과 그에 해당하는 버전들을 딕셔너리로 반환"""
#         asset_versions = {}
#         asset_dirs = os.listdir(ASSET_DIRECTORY)  # ASSET_DIRECTORY에서 모든 파일 리스트 가져오기

#         for asset_name in asset_dirs:
#             asset_versions[asset_name] = AssetManager.get_available_versions(asset_name)

#         return asset_versions
    

#     @staticmethod
#     def get_available_versions(asset_name):
#         """특정 에셋의 모든 버전 가져오기"""
#         asset_dir = AssetManager.get_asset_directory(asset_name)
#         if not asset_dir or not os.path.exists(asset_dir):
#             print(f"⚠️ '{asset_name}'의 디렉토리를 찾을 수 없음.")
#             return "v001"  # 기본값 v001 반환

#         versions = []
#         for file in os.listdir(asset_dir):
#             match = re.search(r"\.v(\d{3})\.(ma|mb)", file)
#             if match:
#                 versions.append(int(match.group(1)))
        
#         print(f"Versions found: {versions}")  # 디버깅 출력  
#         return [f".v{v:03d}" for v in versions] if versions else [".v001"]


#     @staticmethod
#     def get_referenced_asset_paths():
#         """현재 씬에서 참조된 에셋들의 경로를 딕셔너리 형태로 반환"""
#         references = cmds.file(q=True, reference=True) or []
#         asset_paths = {}

#         for ref in references:
#             asset_name = os.path.basename(ref)  # 파일명 추출
#             clean_asset_name = AssetManager.get_clean_asset_name(asset_name)
#             ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)

#             # 에셋 경로를 딕셔너리에 저장
#             asset_paths[clean_asset_name] = ref_path

#         return asset_paths