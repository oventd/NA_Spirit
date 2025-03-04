import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

"""각 스텝에 맞는 match move파일을 불러올 클래스 입니다."""
class MatchMoveStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening match move step")

    def open(self):
        if not cmds.objExists("camera"):
            cmds.camera(cameraShape, q=True, fl=True)
            print("camera group was created.")
        else:
            print("A camera group already exists")

matchmove = MatchMoveStep()
