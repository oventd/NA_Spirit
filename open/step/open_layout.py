import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("layout initialized")

    def open(self):
        self.create_group("char")
        self.create_group("env")
        self.create_group("camera")

        self.reference_file("","char")
        self.reference_file("","env")
        self.reference_file("","camera")

        # 매치무브 카메라
        self.reference_file("", "matchmove_camera")
        self.reference_file("", "matchmove_env")
        
    def create_group(self, group_name):
        if not cmds.objExists(group_name):
            cmds.group(em=True, name=group_name)
            print(f"The {group_name} group was created.")
        else:
            print(f"A {group_name} group already exists.")
    
    def reference_file(self, file_path, group_name):
        if os.path.exists(file_path):
            cmds.file(file_path, name=group_name)
            print(f"The {group_name} {file_path} was referenced.")
        else:
            print(f"The {group_name} {file_path} was not found.")

layout = LayoutStep()
layout.open()

