import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, reference_file, validate_hierarchy  # 유틸 함수 임포트

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("layout initialized")
        self.group_name = None

    def open(self, group_name="env"):
        self.group_name = group_name
        create_group("char")
        create_group(group_name)
        create_group("camera")

        reference_file("","char")
        reference_file("","env")
        reference_file("","camera")

        # 매치무브 카메라
        reference_file("", "matchmove_camera")
        reference_file("", "matchmove_env")

    def validate(self):
        # validate_hierarchy 메서드를 사용하여 환경 그룹과 자식 객체 존재 여부 확인
        if validate_hierarchy(group_name=self.group_name):
            print(f"Validation passed: Env '{self.group_name}' exists.")
        else:
            print(f"Validation failed: Env '{self.group_name}' does not exist.")  

if __name__ == "__main__":
    layout = LayoutStep()
    layout.open()
    layout.validate()

