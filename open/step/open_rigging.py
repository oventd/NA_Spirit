import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

"""각 스텝에 맞는 rig파일을 불러올 클래스 입니다."""
class RiggingStep(StepOpenMaya):
    def __init__(self):
        print("Opening rigging step")

    def open(self):
        self.create_rig_group()

    def create_rig_group(self):
        """rig 그룹을 생성하는 메서드"""
        if not cmds.objExists("rig"):
            cmds.group(em=True, name="rig")
            print("The rig group was created.")
        else:
            print("A rig group already exists.")

rigging = RiggingStep()
rigging.open()