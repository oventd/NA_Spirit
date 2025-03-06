import maya.mel as mel
import maya.cmds as cmds
import os
import sys
from constant import * 
from maya_utils import create_group, reference_file, validate_hierarchy  # 유틸 함수 임포트
sys.path.append(STEP_PATH)
from step_open_maya import StepOpenMaya
sys.path.append(UTILS_PATH)

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("layout initialized")

    class Open:
        @staticmethod
        def setup(group_name=TERRAIN):
            create_group(CHAR)
            create_group(group_name)
            create_group(CAMERA)

            reference_file("",CHAR)
            reference_file("",TERRAIN)
            reference_file("",CAMERA)

            # 매치무브 카메라
            reference_file("", "matchmove_camera")
            reference_file("", "matchmove_env")

    class Publish:
        @staticmethod
        def validate(group_name=TERRAIN):
            validate_hierarchy # 메서드를 사용하여 환경 그룹과 자식 객체 존재 여부 확인
            if validate_hierarchy(group_name=group_name):
                print(f"Validation passed222: Env '{group_name}' exists.")
            else:
                print(f"Validation failed222: Env '{group_name}' does not exist.")  

            if validate_hierarchy(group_name=CAMERA):
                print(f"Validation passed222: Camera group '{group_name}' exists.")
            else:
                print(f"Validation failed222: Camera group '{group_name}' does not exist.")  
            
            pass
if __name__ == "__main__":
    layout = LayoutStep()
    LayoutStep.Open.setup(group_name=TERRAIN)
    LayoutStep.Publish.validate(group_name=TERRAIN)

