import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, create_camera  # 유틸 함수 임포트

"""각 스텝에 맞는 match move 파일을 불러올 클래스입니다."""
class MatchMoveStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening match move step")

    def open(self, group_name="env", camera_group_name="anim_cam", camera_name=None):
        create_group(group_name)
        # create_camera() 호출 시 인자를 키워드 인자로 전달
        create_camera(group_name=camera_group_name, camera_name=camera_name)

if __name__ == "__main__":
    matchmove = MatchMoveStep()
    matchmove.open()
