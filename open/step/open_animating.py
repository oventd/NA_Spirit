import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, reference_file, validate_hierarchy, validate_anim_curve, lock_camera # 유틸 함수 임포트

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    class Open:
        @staticmethod
        def setup(rig_group_name = "rig", terrain_group_name="terrain", camera_group_name="camera"):
            #리그 그룹
            create_group(rig_group_name)
            create_group(terrain_group_name)
            create_group(camera_group_name)

        @staticmethod
        def reference_rig():
            rig_file =""
            reference_file(rig_file, "rig")
        @staticmethod
        def reference_terrain():
            terrain_file =""
            reference_file(terrain_file, "terrain")
        @staticmethod
        def reference_camera():
            camera_file =""
            lock_camera(camera_file)

    class Publish:       
        @staticmethod 
        def validate(rig_group_name = "rig"):
            """Rig 그룹이 존재하는지 확인"""
            if validate_hierarchy(rig_group_name):
                print(f"Validation passed: {rig_group_name} group exists.")
            else:
                print(f"Validation failed: {rig_group_name} group does not exist.")

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