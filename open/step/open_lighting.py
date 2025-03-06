"""세린 웅니 USDLayerEditor가 정말 뉘신지 모르게땀..."""
import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, reference_file, create_usd_proxy  # 유틸 함수 임포트


class Lighting(StepOpenMaya):
    def __init__(self, anim_cache_usd, env_usd):
        super().__init__()
        print("Opening lighting step")
        self.anim_cache_usd = anim_cache_usd
        self.env_usd = env_usd
        # light 그룹 생성
        self.create_lighting_group()

    def open(self):
        print("Opening lighting step")

        # 라이트 그룹 생성 
        create_group("light")
        print("Created light group")

        # animCache usd 로드
        if os.path.exists(self.anim_cache_usd):
            proxy_node = cmds.createNode("mayaUSDProxyShape", name = "animCacheProxy")
            cmds.setAttr(f"{proxy_node}.proxyPath", self.anim_cache_usd, type="string")
            print(f"animCache USD file found: {self.anim_cache_usd}")
        else:
            cmds.warning(f"animCache USD file not found: {self.anim_cache_usd}")
        
        # env usd 레퍼런스
        reference_file(self.env_usd, "environment")

        # Usd Layer Editor 창 오픈
        create_usd_proxy()
        cmds.mayaUsdLayerEditorWindow()
        print("Opened Usd Layer Editor")


if __name__ == "__main__":
    lighting = Lighting()
    anim_cache_usd = "/home/rapa/3D_usd/Kitchen_set/assets/Fork/Fork.usd"
    env_usd = "/home/rapa/3D_usd/Kitchen_set/assets/WallOrange/WallOrange.usd"

    lighting = Lighting(anim_cache_usd, env_usd)
    lighting().open()