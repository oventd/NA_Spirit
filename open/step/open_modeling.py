import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("모델링 불러오기")

    def open(self):
        if not cmds.objExists("geo"):
            cmds.group(em=True, name="geo")
            print("geo 그룹이 생성되었습니다.")
        else:
            print("geo 그룹이 이미 존재합니다.")


modeling = ModelingStep()
modeling.open()
    