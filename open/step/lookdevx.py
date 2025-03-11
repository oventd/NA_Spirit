import maya.cmds as cmds
import maya.mel as mel
import os
import json
import shutil
from pxr import Usd, UsdShade, Sdf

# LookdevX가 있는지 확인
try:
    import lookdevx
    LOOKDEVX_AVAILABLE = True
except ImportError:
    LOOKDEVX_AVAILABLE = False

# 저장할 기본 디렉토리 설정
NAS_SOURCE = r"//nas/char_ref"  # NAS 경로
LOCAL_TARGET = os.path.expanduser("~/maya/lookdev_project")  # 로컬 저장소
SCENE_NAME = "lookdev.mb"

def copy_nas_data():
    """NAS에서 로컬로 Lookdev 데이터를 복사"""
    source_scene = os.path.join(NAS_SOURCE, "scenes", SCENE_NAME)
    target_scene = os.path.join(LOCAL_TARGET, "scenes", SCENE_NAME)

    if not os.path.exists(os.path.dirname(target_scene)):
        os.makedirs(os.path.dirname(target_scene))

    try:
        shutil.copy(source_scene, target_scene)
        print(f"✅ NAS에서 {SCENE_NAME}을 복사 완료: {target_scene}")
        return target_scene
    except Exception as e:
        print(f"❌ NAS 복사 실패: {e}")
        return None

def open_lookdev_scene():
    """Lookdev 씬을 연다."""
    scene_path = copy_nas_data()
    if scene_path and os.path.exists(scene_path):
        cmds.file(scene_path, open=True, force=True)
        print(f"✅ Lookdev 씬 열기 완료: {scene_path}")
    else:
        print("❌ Lookdev 씬을 찾을 수 없습니다.")

def get_shader_assignments():
    """쉐이더가 적용된 메시 정보를 딕셔너리로 반환"""
    shader_mapping = {}

    shading_groups = cmds.ls(type="shadingEngine")
    for sg in shading_groups:
        connected_shaders = cmds.listConnections(f"{sg}.surfaceShader", source=True, destination=False)
        if connected_shaders:
            shader = connected_shaders[0]
            meshes = cmds.listConnections(sg, source=False, destination=True, type="mesh") or []
            shader_mapping[shader] = meshes

    return shader_mapping

def publish_to_lookdevx(shader_mapping):
    """LookdevX에 쉐이더 퍼블리시"""
    if not LOOKDEVX_AVAILABLE:
        print("❌ LookdevX를 사용할 수 없습니다. USD로 내보냅니다.")
        return False

    session = lookdevx.Session()

    for shader, meshes in shader_mapping.items():
        mat = session.createMaterial(shader)
        print(f"✅ LookdevX에 {shader} 퍼블리시 완료")

    session.save()
    return True

def export_shaders_to_usd(shader_mapping, usd_path):
    """쉐이더를 USD로 저장"""
    stage = Usd.Stage.CreateNew(usd_path)

    for shader, meshes in shader_mapping.items():
        shader_path = f"/Materials/{shader}"
        usd_shader = UsdShade.Material.Define(stage, shader_path)

        print(f"✅ USD에 추가됨: {shader_path}")

    stage.GetRootLayer().Save()
    print(f"✅ USD 파일 저장 완료: {usd_path}")

def save_shader_mapping(shader_mapping, json_path):
    """쉐이더와 메시 매핑 정보를 JSON 파일로 저장"""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(shader_mapping, f, indent=4, ensure_ascii=False)
    print(f"✅ 쉐이더 매핑 JSON 저장 완료: {json_path}")

def main():
    """메인 실행 함수"""
    open_lookdev_scene()
    
    shader_mapping = get_shader_assignments()
    if not shader_mapping:
        print("❌ 적용된 쉐이더가 없습니다.")
        return

    scene_name = "lookdev_shaders"
    output_dir = os.path.join(LOCAL_TARGET, "exports")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    usd_path = os.path.join(output_dir, f"{scene_name}.usd")
    json_path = os.path.join(output_dir, f"{scene_name}.json")

    if not publish_to_lookdevx(shader_mapping):
        export_shaders_to_usd(shader_mapping, usd_path)

    save_shader_mapping(shader_mapping, json_path)

# 실행
main()
