import maya.cmds as cmds
import os

def export_usd(file_path):
    """USD 파일을 내보내는 함수 (기본값 제거)"""
    usd_options = ";".join([
        "exportUVs=1",
        "exportSkels=none",
        "exportSkin=none",
        "exportBlendShapes=0",
        "exportDisplayColor=0",
        "filterTypes=nurbsCurve",
        "exportColorSets=0",
        "exportComponentTags=0",
        "animation=0",
        "eulerFilter=0",
        "staticSingleSample=0",
        "startTime=1",
        "endTime=1",
        "frameStride=1",
        "frameSample=0.0",
        "shadingMode=useRegistry",
        "convertMaterialsTo=[MaterialX]",
        "exportMaterials=1",
        "exportAssignedMaterials=1",
        "exportRelativeTextures=automatic",
        "exportInstances=1",
        "exportVisibility=0",
        "mergeTransformAndShape=0",
        "includeEmptyTransforms=0",
        "stripNamespaces=1",
        "worldspace=0",
        "exportStagesAsRefs=0",
        "defaultUSDFormat=usda",
        "excludeExportTypes=[Meshes,Cameras,Lights]"  # ✅ Mesh, Camera, Light 제외
    ])

    # 파일이 저장될 폴더가 존재하는지 확인하고 생성
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # ✅ USD 파일 내보내기 실행
    cmds.file(file_path, force=True, options=usd_options, type="USD Export", preserveReferences=True, exportAll=True)
    print(f"✅ USD exported to: {file_path}")

# 실행 예제
usd_output_path = "/home/rapa/test_maya/Char_Ref/scenes/texture_export.usd"
export_usd(usd_output_path)
