from pxr import Usd

def usd_to_dict(prim):
    """USD의 계층구조를 dict로 변환"""
    return {
        "name": prim.GetName(),
        "type": prim.GetTypeName(),
        "children": {child.GetName(): usd_to_dict(child) for child in prim.GetChildren()}
    }

# USD 파일 로드
usd_file_path = "/home/rapa/NA_Spirit/tex.usd"
stage = Usd.Stage.Open(usd_file_path)

# 계층구조 변환
usd_hierarchy = usd_to_dict(stage.GetPseudoRoot())

# 출력
import json
print(json.dumps(usd_hierarchy, indent=4))
