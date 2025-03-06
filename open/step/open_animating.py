import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group, reference_file, validate_hierarchy # 유틸 함수 임포트

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    def open(self):
        #리그 그룹
        create_group("rig")
        create_group("terrain")
        create_group("camera")

    def validate(self):
        """Rig 그룹과 Terrain 그룹이 존재하는지 확인"""
        if validate_hierarchy("rig"):
            print("Validation passed: 'rig' group exists.")
        else:
            print("Validation failed: 'rig' group does not exist.")
        
        if validate_hierarchy("terrain"):
            print("Validation passed: 'terrain' group exists.")
        else:
            print("Validation failed: 'terrain' group does not exist.")         
            
    def reference_rig(self):
        rig_file =""
        reference_file(rig_file, "rig")
    
    def reference_terrain(self):
        terrain_file =""
        reference_file(terrain_file, "terrain")
    
    def reference_camera(self):
        camera_file =""
        reference_file(camera_file, "camera")

if __name__ == "__main__":
    animation = AnimatingStep()
    animation.open()
    animation.validate()
    animation.reference_camera()