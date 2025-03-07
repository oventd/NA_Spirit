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
        print ("Opening modeling step")

    class Open:
        @staticmethod
        def setup(geo_group_name="geo"):
            create_group(geo_group_name)
            create_group("Low", parent = "geo")
            create_group("High", parent = "geo")

    class Publish:
        @staticmethod
        def validate(geo_group_name="geo", child_list = ["Low", "High"]):
            
            if validate_hierarchy(geo_group_name):
                print(f"Validation passed:'{geo_group_name}' exists.")
            else:
                print(f"Validation failed:'{geo_group_name}' does not exist.")

            if validate_hierarchy(geo_group_name, child_list):
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재합니다.")
            else:
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재하지 않습니다.")


if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup()
    ModelingStep.Publish.validate()
    