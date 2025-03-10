from pxr import Usd, UsdGeom

def get_prim_references(stage, prim_path):
    """ 특정 Prim이 가지고 있는 Reference 리스트를 반환 """
    prim = stage.GetPrimAtPath(prim_path)
    if not prim:
        print(f"Prim not found: {prim_path}")
        return []

    references = prim.GetReferences()
    reference_list = []
    
    for ref in references.GetAddedReferences():
        reference_list.append(ref.assetPath)

    return reference_list
from pxr import Usd, UsdGeom, Sdf

def create_usd_with_references(output_path):
    """ USD 파일을 생성하고 특정 Prim에 Reference 추가 """
    stage = Usd.Stage.CreateNew(output_path)

    # Root Prim 생성
    root_prim = stage.DefinePrim("/Root", "Xform")

    # 참조할 대상 Prim 생성
    referenced_prim_path = "/ReferencedModel"
    referenced_prim = stage.DefinePrim(referenced_prim_path, "Xform")

    # 참조할 USD 파일 생성
    referenced_usd_path = output_path.replace(".usda", "_ref.usda")
    ref_stage = Usd.Stage.CreateNew(referenced_usd_path)
    ref_stage.DefinePrim("/Model", "Xform")
    ref_stage.GetRootLayer().Save()

    # Root Prim에 Reference 추가
    references = root_prim.GetReferences()
    references.AddReference(referenced_usd_path)

    # 저장
    stage.GetRootLayer().Save()
    print(f"USD file created: {output_path}")
    print(f"Referenced USD file created: {referenced_usd_path}")

# 테스트용 USD 파일 생성
create_usd_with_references("test.usda")

# USD 스테이지 열기
usd_file = "test.usda"
stage = Usd.Stage.Open(usd_file)

# 특정 Prim의 Reference 가져오기
prim_path = "/Root/MyPrim"
references = get_prim_references(stage, prim_path)

# 결과 출력
print("References:", references)
