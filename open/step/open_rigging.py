import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
sys.path.append('/home/rapa/NA_Spirit/maya')
sys.path.append('/home/rapa/NA_Spirit/flow')
from maya_utils import MayaUtils
from sg_path_utils import SgPathUtils
from flow_utils import FlowUtils

"""각 스텝에 맞는 match move 파일을 불러올 클래스입니다."""
class RiggingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening rigging step")

    class Open:
        @staticmethod
        def setup(group_name="rig", task_id=None, file_format=".ma"):
            MayaUtils.create_group(group_name)
        # @staticmethod
        # def reference_modeling(task_id=None, file_format="ma"):
            modeling_file = FlowUtils.get_upstream_file_for_currnet_file(task_id, file_format)
            asset_name = os.path.basename(SgPathUtils.trim_entity_path(modeling_file))
            step = SgPathUtils.get_step_from_path(modeling_file)
            name_space = f"{asset_name}_{step}"
            # MayaUtils.reference_file(modeling_file, "modeling")
            if modeling_file:
                MayaUtils.reference_file(modeling_file, name_space) # 원래 저장될때 리네임 되는건가?
            else:
                print(f"⚠ Warning: No published file found for Task ID {task_id} with format {file_format}")
   
    class Publish:
        @staticmethod
        def validate(group_name="rig"):
            """그룹 및 카메라 검증"""

            # 환경 그룹 검증
            if not MayaUtils.validate_hierarchy(group_name):
                print(f"Validation failed: terrain '{group_name}' does not exist.")
                return False
            
            print("Validation passed: 모든 조건을 충족합니다.")
            return True

            # # 카메라 그룹 검증
            # if MayaUtils.validate_hierarchy(group_name=camera_group_name, child_list=[camera_name]):
            #     print(f"Validation passed: Camera '{camera_name}' exists in group '{camera_group_name}'.")
            # else:
            #     print(f"Validation failed: Camera '{camera_name}' does not exist in group '{camera_group_name}'.")

            # # 환경 그룹 검증
            # if MayaUtils.validate_hierarchy(group_name):
            #     print(f"Validation passed: terrain '{group_name}' exists.")
            # else:
            #     print(f"Validation failed: terrain '{group_name}' does not exist.")

        @staticmethod
        def publish():
            print("Publishing rigging step")
            pass

if __name__ == "__main__":
    rigging = RiggingStep()
    RiggingStep.Open.setup()
    RiggingStep.Publish.validate()

#   "MMV": {
#     "module": "open_matchmove",
#     "class": "MatchMoveStep",
#     "path": "/home/rapa/NA_Spirit/open/step/open_matchmove.py"
#   },
#   "LAY": {
#     "module": "open_layout",
#     "class": "LayoutStep",
#     "path": "/home/rapa/NA_Spirit/open/step/open_layout.py"
#   },
#   "ANM": {
#     "module": "open_animating",
#     "class": "AnimatingStep",
#     "path": "/home/rapa/NA_Spirit/open/step/open_animating.py"
#   }

if __name__ == "__main__":
    rigging = RiggingStep()


    file_path = "/nas/spirit/project/spirit/assets/Character/Mat/MDL/publish/usd/scene.usd"
    asset_name = os.path.basename(SgPathUtils.trim_entity_path(file_path))
    step = SgPathUtils.get_step_from_path(file_path)
    name_space = f"{asset_name}_{step}"
    print(name_space)

    ref_nodes = cmds.file("/nas/spirit/project/spirit/assets/Character/Mat/MDL/publish/usd/scene.usd", reference=True, namespace=name_space, returnNewNodes=True)
    print(ref_nodes)
    transform_nodes =[]
    for ref_node in ref_nodes:
        if cmds.objectType(ref_node) in ["transform"]:
            transform_nodes.append(ref_node)
            
    top_node = transform_nodes[0]

    rig_group = cmds.group(name="rig", empty=True)
    cmds.parent(top_node, rig_group)