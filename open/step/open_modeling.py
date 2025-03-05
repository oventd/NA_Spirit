import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import ensure_group  # 유틸 함수 임포트

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("모델링 불러오기")

    def open(self):
        ensure_group("geo")

if __name__ == "__main__":
    modeling = ModelingStep()
    modeling.open()
    