import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

"""각 스텝에 맞는 match move 파일을 불러올 클래스입니다."""
class MatchMoveStep(StepOpenMaya):
    def init(self):
        super().init()
        print("Opening match move step")

    def open(self):
        # 카메라 그룹 생성
        self.create_camera_group()
        # env 그룹 생성
        self.create_env_group()

    def create_camera_group(self):
        """카메라 그룹을 생성하는 메서드"""
        if not cmds.objExists("camera_group"):
            camera_name = cmds.camera()[0]  # 첫 번째 반환 값은 카메라의 이름
            cmds.group(camera_name, name="camera_group")
            print("camera group was created.")
        else:
            print("A camera group already exists.")

    def create_env_group(self):
        """env 그룹을 생성하는 메서드"""
        if not cmds.objExists("env"):
            cmds.group(em=True, name="env")
            print("The env group was created.")
        else:
            print("A env group already exists.")

# MatchMoveStep 객체 생성 및 open 메서드 실행
matchmove = MatchMoveStep()
matchmove.open()
