import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, validate_hierarchy  # 유틸 함수 임포트

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("모델링 불러오기")
        self.group_name = None

    def open(self, group_name="geo"):
        self.group_name = group_name
        create_group(group_name)

    def validate(self):
        if validate_hierarchy(group_name=self.group_name):
            print(f"Validation passed:'{self.group_name}' exists.")
        else:
            print(f"Validation failed:'{self.group_name}' does not exist.")

        if validate_hierarchy("geo", ["Low", "High"]):
            print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재합니다.")
        else:
            print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재하지 않습니다.")


if __name__ == "__main__":
    modeling = ModelingStep()
    modeling.open()
    modeling.validate()
    