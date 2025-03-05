import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import ensure_group, reference_file  # 유틸 함수 임포트

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("layout initialized")

    def open(self):
        ensure_group("char")
        ensure_group("env")
        ensure_group("camera")

        reference_file("","char")
        reference_file("","env")
        reference_file("","camera")

        # 매치무브 카메라
        reference_file("", "matchmove_camera")
        reference_file("", "matchmove_env")

if __name__ == "__main__":
    layout = LayoutStep()
    layout.open()

