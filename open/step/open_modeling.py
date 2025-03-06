import maya.mel as mel
import maya.cmds as cmds
import os
import sys
from constant import * 
from maya_utils import create_group, validate_hierarchy  # 유틸 함수 임포트
sys.path.append(STEP_PATH)
from step_open_maya import StepOpenMaya
sys.path.append(UTILS_PATH)

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("모델링 불러오기")
        self.group_name = None

    class Open:
        @staticmethod
        def setup(group_name=GEO):
            create_group(group_name)
            create_group(LOW, parent = GEO)
            create_group(HIGH, parent = GEO)

    class Publish:
        @staticmethod
        def validate(group_name=GEO):
            if validate_hierarchy(group_name=group_name):
                print(f"Validation passed:'{group_name}' exists.")
            else:
                print(f"Validation failed:'{group_name}' does not exist.")


            if validate_hierarchy(GEO, [LOW, HIGH]):
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재합니다.")
            else:
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재하지 않습니다.")


if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup(group_name=GEO)
    ModelingStep.Publish.validate(group_name=GEO)
    