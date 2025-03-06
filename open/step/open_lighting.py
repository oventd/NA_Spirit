"""세린 웅니 USDLayerEditor가 정말 뉘신지 모르게땀..."""
import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, reference_file  # 유틸 함수 임포트


class Lighting(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening lighting step")

        # light 그룹 생성
        self.create_lighting_group()

    def create_lighting_group(self):
        create_group("lighting")

    def import_ani_cache(self, usd_path):
        # USD 캐시를 USD ProxyNode를 통해 로드
        if not os.path.exists(usd_path):
            cmds.warning(f"USD file not found: {usd_path}")
            return
        proxy_node = cmds.createNode("mayaUsdProxyShape", name= "animCacheProxy")
        cmds.setAttr(f"{proxy_node}.file", usd_path, type="string")
    
    def import_env(self, usd_path): 
        reference_file(usd_path, "environment")

    def open(self):
        cmds.mayaUsdLayerEditorWindow()
        print("Open Usd Layer Editor")
    


if __name__ == "__main__":
    lighting = Lighting()

    lighting().open()