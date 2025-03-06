import maya.mel as mel
import maya.cmds as cmds
import os
import sys
from constant import *
from maya_utils import create_group, reference_file, validate_hierarchy, validate_anim_curve, lock_camera # 유틸 함수 임포트
sys.path.append(STEP_PATH)
from step_open_maya import StepOpenMaya
sys.path.append(UTILS_PATH)

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    class Open:
        @staticmethod
        def setup():
            #리그 그룹
            create_group(RIG)
            create_group(TERRAIN)
            create_group(CAMERA)

        @staticmethod
        def reference_rig():
            rig_file =""
            reference_file(rig_file, RIG)
        @staticmethod
        def reference_terrain():
            terrain_file =""
            reference_file(terrain_file, TERRAIN)
        @staticmethod
        def reference_camera():
            camera_file =""
            lock_camera(camera_file)

    class Publish:       
        @staticmethod 
        def validate():
            """Rig 그룹이 존재하는지 확인"""
            if validate_hierarchy(RIG):
                print("Validation passed: 'rig' group exists.")
            else:
                print("Validation failed: 'rig' group does not exist.")

            # animCurveTL 노드 확인
            if validate_anim_curve():
                print("Validation passed: 'animCurveTL' node exists.")
            else:
                print("Validation failed: 'animCurveTL' node does not exist.")
                 
                

if __name__ == "__main__":
    animation = AnimatingStep()
    AnimatingStep.Open.setup()
    AnimatingStep.Open.reference_rig()
    AnimatingStep.Open.reference_terrain()
    AnimatingStep.Open.reference_camera()
    AnimatingStep.Publish.validate()