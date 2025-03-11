import maya.cmds as cmds
import os
import sys

# 경로 설정
utils_dir = '/home/rapa/NA_Spirit/utils'
sys.path.append(utils_dir)
usd_dir = '/home/rapa/NA_Spirit/usd/'
sys.path.append(usd_dir)

# 외부 모듈 임포트
from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils
from published_version_usd_connector import PublishUsd2StepUsdConnector


def print_references():
    """현재 씬의 모든 Reference 정보를 출력"""
    references = cmds.ls(type="reference")

    if not references:
        print("No references found in the scene.")
        return

    for ref in references:
        ref_path = cmds.referenceQuery(ref, filename=True)
        is_loaded = cmds.referenceQuery(ref, isLoaded=True)
        associated_nodes = cmds.referenceQuery(ref, nodes=True) or []

        print(f"Reference Node: {ref}")
        print(f"  File Path: {ref_path}")
        print(f"  Loaded: {is_loaded}")
        print(f"  Associated Nodes: {associated_nodes}\n")

def get_anim_curve_tl_nodes():
    """모든 애니메이션 커브의 value 연결된 트랜스폼 노드를 가져옴"""
    anim_curves = cmds.ls(type="animCurve")
    tl_nodes = set()

    for anim_curve in anim_curves:
        value_node = cmds.listConnections(f"{anim_curve}.output", source=False, destination=True)
        if value_node:
            tl_nodes.add(value_node[0])

    return list(tl_nodes)

def get_parent_hierarchy(obj):
    """주어진 오브젝트의 부모 계층을 리스트로 반환 (최상위 Root까지)"""
    hierarchy = []
    current_obj = obj

    while True:
        parent = cmds.listRelatives(current_obj, parent=True)
        if not parent:
            break
        hierarchy.append(parent[0])
        current_obj = parent[0]

    return hierarchy

def find_scene_animation_range():
    """씬에서 애니메이션 프레임 범위를 찾음"""
    animation_curves = cmds.ls(typ="animCurve")

    if not animation_curves:
        return 1, 1

    start = int(cmds.playbackOptions(q=True, min=True))
    end = int(cmds.playbackOptions(q=True, max=True))

    return start, end

# 실행
print_references()
tl_nodes = get_anim_curve_tl_nodes()

print("Time, Value Nodes:", tl_nodes)

# 선택된 오브젝트 확인 및 계층 관계 추출
selected_objects = tl_nodes
key_existing_objects = []
if selected_objects:
    for obj in selected_objects:
        hierarchy = get_parent_hierarchy(obj)
        if len(hierarchy) >= 3:
            key_existing_objects.append(hierarchy[-3])  # 인덱스 에러 방지
else:
    print("No object selected.")

print("Key existing:", key_existing_objects)

# USD 생성 및 연결
root_path = "/home/rapa/NA_Spirit"
usd_test_path = os.path.join(root_path, "test2.usd")

if not os.path.exists(usd_test_path):
    UsdUtils.create_usd_file(usd_test_path)

stage = UsdUtils.get_stage(usd_test_path)


# Assets 존재 여부 확인
assets = "Assets"
if not cmds.objExists(assets):
    raise ValueError("Assets node does not exist.")

categorys = cmds.listRelatives(assets, children=True) or []
assets_scope = UsdUtils.create_scope(stage, "/"+assets)
assets_scope_path = UsdUtils.get_prim_path(assets_scope)
for category in categorys:
    category_scope = UsdUtils.create_scope(stage, f"{assets_scope_path}/{category}")
    category_scope_path = UsdUtils.get_prim_path(category_scope)
    assets = cmds.listRelatives(category, children=True) or []
    for asset in assets:
        print(asset)
        asset_name = asset.split(":")[0]
        ref_node = cmds.referenceQuery(asset, referenceNode=True)
        ref_path = cmds.referenceQuery(ref_node, filename=True)

        ref_version = SgPathUtils.get_version(ref_path)
        usd_path = ref_path.replace("maya", "usd")
        mod_path = SgPathUtils.set_step(usd_path, MDL)
        mod_usd_dir = os.path.dirname(mod_path)
        mod_usd_path = os.path.splitext(mod_path)[0].split(".")[0] + ".usd"

        if not os.path.exists(mod_usd_path):
            raise ValueError(f"USD file not found: {mod_usd_path}")

        print("Checking USD directory:", mod_usd_dir)

        for usd in os.listdir(mod_usd_dir):
            if mod_usd_path in usd:
                print(f"USD found: {usd}")
                break

        usd_root_dir = os.path.dirname(mod_path)
        usd_list = os.listdir(usd_root_dir)

        # 루트 트랜스폼 가져오기
        root_curve = f"{asset.split(':')[0]}:root"
        root_curve_transform = {attr: cmds.getAttr(f"{root_curve}.{attr}") for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']}
        print("Root Curve Transform:", root_curve_transform)

        print("USD Root Dir:", usd_root_dir)

        if asset in key_existing_objects:
            print(f"{asset_name} is a key existing object.")
        else:
            print(f"{asset_name} is not a key existing object. Creating Xform and adding reference.")
            
            xform = UsdUtils.create_xform(stage, f"{category_scope_path}/{asset_name}")
            print(f"Created Xform: {asset_name}")
            print(mod_usd_path)
            UsdUtils.add_reference(xform, mod_usd_path)
            print(f"Added reference: {mod_usd_path}")
            root_translate = (root_curve_transform['tx'], root_curve_transform['ty'], root_curve_transform['tz'])
            root_rotate = (root_curve_transform['rx'], root_curve_transform['ry'], root_curve_transform['rz'])
            root_scale = (root_curve_transform['sx'], root_curve_transform['sy'], root_curve_transform['sz'])

            UsdUtils.set_transform(xform, translate=root_translate, rotate=root_rotate, scale=root_scale)
            print("Set Transform")
