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
    @staticmethod
    def __init__(self, env_usd):
        super().__init__()
        print("Opening lighting step")
        self.env_usd = env_usd
        # light 그룹 생성
        self.create_lighting_group()

    def open(self):
        print("Opening lighting step")

        # 라이트 그룹 생성 
        create_group("light")
        print("Created light group")

        # usd 로드
        create_usd_proxy()

        # env usd 레퍼런스
        reference_file(self.env_usd, "environment")
        print("Opened Usd Layer Editor")


if __name__ == "__main__":
    env_usd = "/home/rapa/3D_usd/Kitchen_set/assets/WallOrange/WallOrange.usd"

    lighting = Lighting(env_usd)
    lighting().open()