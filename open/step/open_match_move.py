import maya.cmds as cmds
import os
import sys
sys.path.append(STEP_PATH)
from step_open_maya import StepOpenMaya
sys.path.append(UTILS_PATH)
from constant import * 
from maya_utils import create_group, create_camera, validate_hierarchy  # 유틸 함수 임포트

"""각 스텝에 맞는 match move 파일을 불러올 클래스입니다."""
class MatchMoveStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening match move step")

    class Open:
        @staticmethod
        def setup(group_name=ENV, camera_group_name="anim_cam", camera_name=None):
            group_name = group_name
            camera_group_name = camera_group_name
            create_group(group_name)
            camera_name = create_camera(group_name=camera_group_name, camera_name=camera_name)
    class Publish:
        @staticmethod
        def validate(group_name=ENV, camera_group_name="anim_cam", camera_name="camera1"):
            """그룹 및 카메라 검증"""
            if not camera_name:
                camera_name = "camera1"  # 기본 카메라 이름으로 설정

            # 카메라 그룹 검증
            if validate_hierarchy(group_name=camera_group_name, valid_list=[camera_name]):
                print(f"Validation passed: Camera '{camera_name}' exists in group '{camera_group_name}'.")
            else:
                print(f"Validation failed: Camera '{camera_name}' does not exist in group '{camera_group_name}'.")

            # 환경 그룹 검증
            if validate_hierarchy(group_name=group_name):
                print(f"Validation passed: Env '{group_name}' exists.")
            else:
                print(f"Validation failed: Env '{group_name}' does not exist.") 

if __name__ == "__main__":
    matchmove = MatchMoveStep()
    MatchMoveStep.Open.setup(group_name=ENV)
    MatchMoveStep.Publish.validate(group_name=ENV, camera_name=camera_name)