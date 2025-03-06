import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, create_camera, validate_hierarchy  # 유틸 함수 임포트

"""각 스텝에 맞는 match move 파일을 불러올 클래스입니다."""
class MatchMoveStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening match move step")

        self.group_name = None
        self.camera_group_name = None
        self.camera_name = None

    def open(self, group_name="env", camera_group_name="anim_cam", camera_name=None):
        self.group_name = group_name
        self.camera_group_name = camera_group_name
        create_group(group_name)
        self.camera_name = create_camera(group_name=self.camera_group_name, camera_name=camera_name)

    def validate(self):
        """그룹 및 카메라 검증"""
        if not self.camera_name:
            self.camera_name = "camera1"  # 기본 카메라 이름으로 설정

        # 카메라 그룹 검증
        if validate_hierarchy(group_name=self.camera_group_name, valid_list=[self.camera_name]):
            print(f"Validation passed: Camera '{self.camera_name}' exists in group '{self.camera_group_name}'.")
        else:
            print(f"Validation failed: Camera '{self.camera_name}' does not exist in group '{self.camera_group_name}'.")

        # 환경 그룹 검증
        if validate_hierarchy(group_name=self.group_name):
            print(f"Validation passed: Env '{self.group_name}' exists.")
        else:
            print(f"Validation failed: Env '{self.group_name}' does not exist.") 

if __name__ == "__main__":
    matchmove = MatchMoveStep()
    matchmove.open()
    matchmove.validate()
