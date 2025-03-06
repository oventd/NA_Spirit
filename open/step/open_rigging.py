import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, validate_hierarchy # 유틸 함수 임포트

"""각 스텝에 맞는 rig파일을 불러올 클래스 입니다."""
class RiggingStep(StepOpenMaya):
    def __init__(self):
        print("Opening rigging step")
        self.group_name = None

    def open(self, group_name="rig"):
        self.group_name = group_name
        create_group(group_name)

    def validate(self):
        if validate_hierarchy(group_name=self.group_name):
            print(f"Validation passed: Rig '{self.group_name}' exists.")
        else:
            print(f"Validation failed: Rig '{self.group_name}' does not exist.")         
        

# 네임 메인
if __name__ == "__main__":
    rigging = RiggingStep()
    rigging.open()
    rigging.validate()