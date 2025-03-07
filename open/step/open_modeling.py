import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import MayaUtils

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Opening modeling step")

    class Open:
        @staticmethod
        def setup(geo_group_name="geo"):
            MayaUtils.create_group(geo_group_name)
            MayaUtils.create_group("Low", parent = "geo")
            MayaUtils.create_group("High", parent = "geo")

    class Publish:
        @staticmethod
        def validate(geo_group_name="geo", child_list = ["Low", "High"]):
            
            if MayaUtils.validate_hierarchy(geo_group_name):
                print(f"Validation passed:'{geo_group_name}' exists.")
            else:
                print(f"Validation failed:'{geo_group_name}' does not exist.")

            if MayaUtils.validate_hierarchy(geo_group_name, child_list):
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재합니다.")
            else:
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재하지 않습니다.")


if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup()
    ModelingStep.Publish.validate()
    