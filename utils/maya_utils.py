import maya.cmds as cmds
import os  # os 모듈 임포트 추가

"""maya에서 공통 기능을 모아둔 메서드입니다."""
def ensure_group(name, parent=None):
    """
    특정 그룹이 존재하지 않으면 생성하는 함수.
    :param name: 생성할 그룹 이름
    :param parent: 부모 그룹 (기본값: None)
    """
    if not cmds.objExists(name):
        if parent:
            cmds.group(em=True, name=name, parent=parent)
        else:
            cmds.group(em=True, name=name)
        print(f"Group '{name}' was created.")
    else:
        print(f"Group '{name}' already exists.")

def ensure_camera(group_name, camera_name=None):
    """
    카메라 그룹과 카메라가 없으면 생성하는 함수.
    :param group_name: 생성할 카메라 그룹 이름 (반드시 지정해야 함)
    :param camera_name: 생성할 카메라 이름 (기본값: None이면 새 카메라 자동 생성)
    """
    if not group_name:
        raise ValueError("group_name must be specified for ensure_camera.")

    # 카메라 이름이 None이면 새 카메라를 생성
    if camera_name is None or not cmds.objExists(camera_name):
        camera_name = cmds.camera()[0]  # 새 카메라 생성 후 첫 번째 반환값 사용
        print(f"New camera '{camera_name}' was created.")

    # 그룹이 존재하지 않으면 생성 후 카메라 추가
    if not cmds.objExists(group_name):
        cmds.group(camera_name, name=group_name)
        print(f"Camera group '{group_name}' was created with camera '{camera_name}'.")
    else:
        print(f"Camera group '{group_name}' already exists.")

def reference_file(file_path, group_name):
    """
    특정 파일이 존재하면 해당 파일을 Maya에 참조하는 함수.
    :param file_path: 참조할 파일의 경로
    :param group_name: 참조할 그룹의 이름
    """
    if os.path.exists(file_path):
        cmds.file(file_path, reference=True)
        print(f"The {group_name} file '{file_path}' was referenced.")
    else:
        print(f"The {group_name} file '{file_path}' was not found.")