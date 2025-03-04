import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

class ModelingStep(StepOpenMaya):
    def __init__(self):
        pass

    def open(self):
        print("Opening modeling step...")


if __name__ == "__main__":
    step = ModelingStep()
    step.open()
    