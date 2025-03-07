import maya.cmds as cmds
import os  # os 모듈 임포트 추가

"""maya에서 공통 기능을 모아둔 메서드입니다."""
def create_group(name, parent=None):
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

def create_camera(group_name, camera_name=None):
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
    return camera_name

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

def reference_camera(camera_file):
    """카메라 파일 참조하고, 카메라 락 설정"""
    if os.path.exists(camera_file):
        cmds.file(camera_file, reference=True)  # 파일 참조
        camera_name = cmds.ls(type="camera")[0]  # 첫 번째 카메라 찾기
        if camera_name:
            cmds.lockNode(camera_name, lock=True)  # 카메라 락 설정
            print(f"The camera layout file '{camera_file}' was referenced and locked.")
        else:
            print("No camera found in the scene to lock.")
    else:
        print(f"The camera layout file '{camera_file}' was not found.")

def validate_hierarchy(group_name, valid_list=None):
    """
    특정 그룹과 자식 객체들이 존재하는지 확인하는 함수.
    :param group_name: 부모 그룹 이름
    :param valid_list: 확인할 자식 그룹들의 이름들 (가변 인자)
    :return: 그룹이 존재하고, 자식 그룹들이 모두 존재하면 True, 아니면 False
    """
    # valid_list가 None이면 빈 리스트로 설정
    if valid_list is None:
        valid_list = []

    # 그룹 존재 여부 확인
    if not cmds.objExists(group_name):
        print(f"Validation failed: Group '{group_name}' does not exist.")
        return False
    else:
        print(f"Validation passed: Group '{group_name}' exists.")

    # 자식 그룹들이 있을 경우에만 확인
    if valid_list:
        # 자식 객체들의 목록 가져오기
        existing_children = cmds.listRelatives(group_name, children=True, fullPath=False) or []
        
        # 각 자식 그룹들이 존재하는지 확인
        for child in valid_list:
            if child not in existing_children:
                print(f"Validation failed: '{child}' does not exist under group '{group_name}'.")
                return False
            
    # 그룹이 비어있는지 확인 (자식이 없는 경우)
    existing_children = cmds.listRelatives(group_name, children=True, fullPath=False) or []
    if not existing_children:
        print(f"Validation passed: Group '{group_name}' exists but is empty.")
        return False

    return True

def validate_anim_curve():
    """animCurveTL 노드가 존재하는지 확인하는 함수"""
    if not cmds.objExists("animCurveTL"):
        print("Validation failed: 'animCurveTL' node does not exist.")
        return False
    else:
        print("Validation passed: 'animCurveTL' node exists.")
        return True
def create_lighting_group():
    create_group("light")
    print("Created lighting group")


def create_usd_proxy(usd_file, proxy_name="mayaUsdProxyShape"):
    # 기존에 같은 이름의 mayaUsdProxyShape 노드가 있는지 확인
    existing_nodes = cmds.ls(type="mayaUsdProxyShape")
    
    if existing_nodes:
        print(f"Existing USD Proxy Node found: {existing_nodes[0]}")
        proxy_node = existing_nodes[0]
    else:
        # 새로운 노드 생성
        proxy_node = cmds.createNode("mayaUsdProxyShape", name=proxy_name)
        print(f"Created USD Proxy Node: {proxy_node}")

    # USD 파일 경로 설정
        cmds.setAttr(f"{proxy_node}.filePath", usd_file, type="string")
        print(f"USD Proxy Node linked to: {usd_file}")

