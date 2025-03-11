import maya.cmds as cmds
import os
import sys
utils_dir = '/home/rapa/NA_Spirit/utils'
sys.path.append(utils_dir)

from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils
def print_references():
    """현재 씬의 모든 Reference 정보를 출력"""
    # 씬에서 로드된 모든 레퍼런스 가져오기
    references = cmds.ls(type="reference")

    if not references:
        print("No references found in the scene.")
        return
    
    for ref in references:
        # 레퍼런스 파일 경로 가져오기
        ref_path = cmds.referenceQuery(ref, filename=True)
        # 레퍼런스가 로드되어 있는지 확인
        is_loaded = cmds.referenceQuery(ref, isLoaded=True)
        # 연결된 노드 가져오기
        associated_nodes = cmds.referenceQuery(ref, nodes=True) or []

        print(f"Reference Node: {ref}")
        print(f"  File Path: {ref_path}")
        print(f"  Loaded: {is_loaded}")
        print(f"  Associated Nodes: {associated_nodes}\n")
def get_anim_curve_tl_nodes():
    """모든 애니메이션 커브의 time, value 노드를 가져옵니다."""
    anim_curves = cmds.ls(type="animCurve")
    tl_nodes = []

    for anim_curve in anim_curves:
        # 애니메이션 커브의 time, value 노드 가져오기
        value_node = cmds.listConnections(f"{anim_curve}.output", source=False, destination=True)

        if value_node:
            if value_node[0] in tl_nodes:
                continue
            tl_nodes.append(value_node[0])

    return tl_nodes
import maya.cmds as cmds

def get_parent_hierarchy(obj):
    """주어진 오브젝트의 부모 계층을 리스트로 반환 (최상위 Root까지)"""
    hierarchy = []
    current_obj = obj

    while True:
        parent = cmds.listRelatives(current_obj, parent=True)  # 부모 가져오기
        if not parent:  # 부모가 없으면 최상위 노드이므로 종료
            break
        hierarchy.append(parent[0])  # 부모를 리스트에 추가
        current_obj = parent[0]  # 다음 부모를 탐색

    return hierarchy


def find_scene_animation_range():
    """
    Find the animation range from the current scene.
    """
    # look for any animation in the scene:
    animation_curves = cmds.ls(typ="animCurve")

    # if there aren't any animation curves then just return
    # a single frame:
    if not animation_curves:
        return 1, 1

    # something in the scene is animated so return the
    # current timeline.  This could be extended if needed
    # to calculate the frame range of the animated curves.
    start = int(cmds.playbackOptions(q=True, min=True))
    end = int(cmds.playbackOptions(q=True, max=True))

    return start, end

# 실행
print_references()
tl_nodes = get_anim_curve_tl_nodes()


print("Time, Value Nodes:", tl_nodes)

# 테스트 실행
selected_objects = tl_nodes
key_existing_objects = []
if selected_objects:
    for obj in selected_objects:
        hierarchy = get_parent_hierarchy(obj)
        key_existing_objects.append(hierarchy[-3])
        

else:
    print("No object selected.")

print("key existing: ",key_existing_objects)

root_path = "/home/rapa/NA_Spirit"
usd_test_path = os.path.join(root_path, "test.usda")
if not os.path.exists(usd_test_path):
    UsdUtils.create_usd_file(os.path.join(usd_test_path))
stage = UsdUtils.get_stage(os.path.join(usd_test_path))
UsdUtils.create_scope(stage, "/Root")

if not cmds.objExists("Assets"):
    raise ValueError("Assets already exists.")
types = cmds.listRelatives("Assets", children=True)
assets = cmds.listRelatives(types, children=True)
for asset in assets:
    print(asset)
    if asset in key_existing_objects:
        print("Key existing object found.")
        break
    else:
        print("Key existing object not found.")

