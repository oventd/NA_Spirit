import maya.mel as mel
import maya.cmds as cmds
import os
import sys
from constant import * 
from maya_utils import create_group, validate_hierarchy # 유틸 함수 임포트
sys.path.append(STEP_PATH)
from step_open_maya import StepOpenMaya
sys.path.append(UTILS_PATH)

"""각 스텝에 맞는 rig파일을 불러올 클래스 입니다."""
class RiggingStep(StepOpenMaya):
    def __init__(self):
        print("Opening rigging step")

    class Open:
        @staticmethod
        def setup(group_name=RIG):
            create_group(group_name)
            
    class Publish:
        @staticmethod
        def validate(group_name=RIG):
            # 그룹이 존재하고 비어 있지 않은지 확인
            if validate_hierarchy(group_name=group_name):
                print(f"Validation passed: Rig '{group_name}' exists and is not empty.")
            else:
                print(f"Validation failed: Rig '{group_name}' does not exist or is empty.")

        

# 네임 메인
if __name__ == "__main__":
    rigging = RiggingStep()
    RiggingStep.Open.setup(group_name=RIG)
    RiggingStep.Publish.validate(group_name=RIG)