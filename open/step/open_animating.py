import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import MayaUtils
from sg_path_utils import SgPathUtils

class AnimatingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Animating initialized")

    class Open:
        @staticmethod
        def setup(rig_group_name = "rig", terrain_group_name="terrain", camera_group_name="camera"):
            #리그 그룹
            MayaUtils.create_group(rig_group_name)
            MayaUtils.create_group(terrain_group_name)
            MayaUtils.create_group(camera_group_name)

        @staticmethod
        def reference_rig():
            rig_file =""
            MayaUtils.reference_file(rig_file, "rig")
        
        @staticmethod
        def reference_terrain():
            terrain_file =""
            MayaUtils.reference_file(terrain_file, "terrain")

        @staticmethod
        def reference_camera():
            camera_file = ""  # 경로 설정
            camera_objects = MayaUtils.reference_file(camera_file, "camera")
            
            if camera_objects:  # 카메라 오브젝트가 있을 때만
                MayaUtils.lock_transform([camera_objects])
            else:
                print("No camera objects found to lock.")

    class Publish:       
        @staticmethod 
        def validate(rig_group_name = "rig"):
            """Rig 그룹이 존재하는지 확인"""
            if not MayaUtils.validate_hierarchy(rig_group_name):
                print(f"Validation failed: {rig_group_name} group does not exist.")
                return False

            # animCurveTL 노드 확인
            if not MayaUtils.validate_anim_curve():
                print("Validation failed: 'animCurveTL' node does not exist.")
                return False
            
            print("Validation passed: 모든 조건을 충족합니다.")
            return True

            # if not MayaUtils.validate_hierarchy(rig_group_name):
            #     print(f"Validation passed: {rig_group_name} group exists.")
            # else:
            #     print(f"Validation failed: {rig_group_name} group does not exist.")

            # # animCurveTL 노드 확인
            # if MayaUtils.validate_anim_curve():
            #     print("Validation passed: 'animCurveTL' node exists.")
            # else:
            #     print("Validation failed: 'animCurveTL' node does not exist.")
                
        def publish(rig_group_name = "rig", export_path="/home/rapa/3D_usd/Overwatch_2_-_Ramattra"):
            if not cmds.objExists(rig_group_name):
                print(f"Error: Group '{rig_group_name}' does not exist.")
                return False
            
            cmds.select("rig")
            cmds.file(
                export_path,
                force=True,
                type="USD Export",
                exportSelected=True
                )
            print(f"{export_path}에서 USD export 완료")
            
            

                

if __name__ == "__main__":
    animation = AnimatingStep()
    AnimatingStep.Open.setup()
    AnimatingStep.Open.reference_rig()
    AnimatingStep.Open.reference_terrain()
    AnimatingStep.Open.reference_camera()
    AnimatingStep.Publish.validate()