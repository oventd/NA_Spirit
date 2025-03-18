import maya.cmds as cmds
import json
import os

def get_usd_preview_surface_assignments():
    """USD Preview Surface 노드만 필터링하여 할당된 오브젝트 목록을 JSON 형식으로 저장"""
    usd_preview_dict = {}

    # 모든 쉐이딩 그룹 가져오기
    shading_groups = cmds.ls(type="shadingEngine")

    for sg in shading_groups:
        # 쉐이딩 그룹에 연결된 머티리얼 가져오기
        materials = cmds.listConnections(sg + ".surfaceShader", source=True, destination=False) or []
        
        for material in materials:
            # USD Preview Surface 노드만 필터링
            if cmds.nodeType(material) == "usdPreviewSurface":
                # 해당 머티리얼이 적용된 지오메트리 찾기
                objects = cmds.sets(sg, query=True) or []
                usd_preview_dict[material] = objects

    return usd_preview_dict

def save_usd_preview_surface_to_json(json_path):
    """USD Preview Surface 할당 정보를 JSON 파일로 저장"""
    usd_preview_data = get_usd_preview_surface_assignments()

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(usd_preview_data, json_file, indent=4, ensure_ascii=False)

    print(f" USD Preview Surface 데이터가 {json_path}에 저장되었습니다.")

# 실행 예제
if __name__ == "__main__":
    json_output_path = os.path.join("D:\\real\\char_ref", "usd_preview_surface_assignments.json")
    save_usd_preview_surface_to_json(json_output_path)
