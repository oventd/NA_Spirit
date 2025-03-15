import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import MayaUtils
from sg_path_utils import SgPathUtils

class LayoutStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("layout initialized")

    class Open:
        @staticmethod
        def setup(terrain_group_name="terrain", camera_group_name="camera", rig_group_name = "rig"):
            MayaUtils.create_group(rig_group_name)
            MayaUtils.create_group(terrain_group_name)
            MayaUtils.create_group(camera_group_name)

            MayaUtils.reference_file("","rig")
            MayaUtils.reference_file("","terrain")
            MayaUtils.reference_file("","camera")

            # 매치무브 카메라
            MayaUtils.reference_file("", "matchmove_camera")
            MayaUtils.reference_file("", "matchmove_env")

    class Publish:
        @staticmethod
        def validate(rig_group_name = "rig", terrain_group_name="terrain", camera_group_name="camera"):
            
            exception_group = {"rig"} # 검증 예외처리 할 객체

            # rig 그룹이 존재하는지 체크
            if not MayaUtils.validate_hierarchy(rig_group_name, exception_group=exception_group):
                print(f"Validation failed: Rig group '{rig_group_name}' does not exist.")  
                return False

            # terrain 그룹이 존재하는지 체크
            if MayaUtils.validate_hierarchy(terrain_group_name):
                print(f"Validation failed: terrain '{terrain_group_name}' does not exist.")  
                return False

            # camera 그룹이 존재하는지 체크
            if MayaUtils.validate_hierarchy(camera_group_name):
                print(f"Validation failed: Camera group '{camera_group_name}' does not exist.")  
                return False  

            # # rig 그룹이 존재하는지 체크
            # if MayaUtils.validate_hierarchy(rig_group_name, exception_group=exception_group):
            #     print(f"Validation passed: Rig group '{rig_group_name}' exists.")
            # else:
            #     print(f"Validation failed: Rig group '{rig_group_name}' does not exist.")  

            # # terrain 그룹이 존재하는지 체크
            # if MayaUtils.validate_hierarchy(terrain_group_name):
            #     print(f"Validation passed: terrain '{terrain_group_name}' exists.")
            # else:
            #     print(f"Validation failed: terrain '{terrain_group_name}' does not exist.")  

            # # camera 그룹이 존재하는지 체크
            # if MayaUtils.validate_hierarchy(camera_group_name):
            #     print(f"Validation passed: Camera group '{camera_group_name}' exists.")
            # else:
            #     print(f"Validation failed: Camera group '{camera_group_name}' does not exist.") 
        
        @staticmethod
        def publish(session_path: str ):
            """ 특정 그룹을 USD와 MB 파일로 export """
            step = SgPathUtils.get_step_from_path(session_path)
            category = SgPathUtils.get_category_from_path(session_path)
            return True

            
if __name__ == "__main__":
    layout = LayoutStep()
    LayoutStep.Open.setup()
    LayoutStep.Publish.validate()

