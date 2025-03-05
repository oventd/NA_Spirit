import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import ensure_group  # 유틸 함수 임포트

"""각 스텝에 맞는 rig파일을 불러올 클래스 입니다."""
class RiggingStep(StepOpenMaya):
    def __init__(self):
        print("Opening rigging step")

    def open(self):
        ensure_group("rig")

# 네임 메인
if __name__ == "__main__":
    rigging = RiggingStep()
    rigging.open()