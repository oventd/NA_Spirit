import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("모델링 불러오기")

    def open(self):
        if not cmds.objExists("layout"):
            cmds.group(em=True, name="layout")
            print("The layout group was created.")
        else:
            print("A layout group already exists.")


layout = LayoutStep()
layout.open()
    