"""세린 웅니 USDLayerEditor가 정말 뉘신지 모르게땀..."""
import maya.mel as mel
import maya.cmds as cmds
import os
import sys

sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import  reference_file, create_usd_proxy, create_lighting_group # 유틸 함수 임포트


class Lighting(StepOpenMaya):
    def __init__(self, env_usd):
        super().__init__()
        print("Opening lighting step")
        self.env_usd = env_usd

    def open(self):

        print("Opening lighting step")

    
        # 라이트 그룹 생성 
        create_lighting_group()

        # usd 로드
        create_usd_proxy(None)

        # env USD 파일이 존재하는지 확인 후 레퍼런스
        if not os.path.exists(self.env_usd):
            cmds.warning(f"Environment USD file not found: {self.env_usd}")
        else:
            reference_file(self.env_usd, "environment")

        # USD Layer Editor 실행 전 플러그인 확인
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")

        cmds.mayaUsdLayerEditorWindow()
        print("Opened USD Layer Editor")



if __name__ == "__main__":
    env_usd = "/home/rapa/3D_usd/Kitchen_set/assets/WallOrange/WallOrange.usd"

    lighting = Lighting(env_usd)
    lighting.open()