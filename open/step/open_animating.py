import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import ensure_group, ensure_camera, reference_file  # 유틸 함수 임포트

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    def open(self):
        #리그 그룹
        ensure_group("rig")
        ensure_group("terrain")
        ensure_group("camera")
        self.reference_camera()
            
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
        