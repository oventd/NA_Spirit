import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    def open(self):
        #리그 그룹
        if not cmds.objExists("rig"):
            cmds.group(em=True, name="rig")
            print("The rig group was created.")
        else:
            print("A rig group already exists.")
        # terrain 그룹
        if not cmds.objExists("terrain"):
            cmds.group(em=True, name="terrain")
            print("The terrain group was created.")
        else:
            print("A terrain group already exists.")
        
        # camera 그룹
        if not cmds.objExists("camera"):
            cmds.group(em=True, name="camera")
            print("The camera group was created.")
            self.reference_camera()
    
        else:
            print("A camera group already exists.")
            
    def reference_rig(self):
        rig_file =""
        if os.path.exists(rig_file):
            cmds.file(rig_file, name="rig")
            print("The rig {rig_file} was referenced.")
        else:
            print("The rig {rig_file} was not found.")
    
    def reference_terrain(self):
        terrain_file =""
        if os.path.exists(terrain_file):
            cmds.file(terrain_file, reference=True, namesapce="terrain")
            print("The terrain {terrain_file} was referenced.")
        else:
            print("The terrain {terrain_file} was not found.")
    
    def reference_camera(self):
        camera_file =""
        if os.path.exists(camera_file):
            cmds.file(camera_file, reference=True, namesapce="camera")
            print("The camera {camera_file} was referenced.")
        else:
            print("The camera {camera_file} was not found.")


animation = AnimatingStep()
animation.open()
    