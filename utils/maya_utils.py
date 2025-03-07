import maya.cmds as cmds
import os  # os 모듈 임포트 추가

class MayaUtils:
    """maya에서 공통 기능을 모아둔 메서드입니다."""

    @staticmethod
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

    @staticmethod
    def create_camera(group_name=None, camera_name=None):
        """
        카메라 그룹과 카메라가 없으면 생성하는 함수.
        :param group_name: 카메라를 넣을 그룹 이름 (None이면 그룹 생성 안 함)
        :param camera_name: 생성할 카메라 이름 (None이면 자동 생성)
        """
        # 카메라가 이미 존재하면 그대로 사용
        if camera_name and cmds.objExists(camera_name):
            print(f"Using existing camera: '{camera_name}'")
        else:
            # 카메라가 존재하지 않으면 새로 생성
            new_camera = cmds.camera()[0]  # 새 카메라 생성
            if camera_name:
                camera_name = cmds.rename(new_camera, camera_name)  # 원하는 이름으로 변경
            else:
                camera_name = new_camera  # Maya 기본 이름 사용
            print(f"New camera '{camera_name}' was created.")

        # 그룹이 존재하면 카메라를 페어런트, 없으면 그룹 생성 후 페어런트
        if group_name:
            if cmds.objExists(group_name):
                parent = cmds.listRelatives(camera_name, parent=True)
                if parent and parent[0] == group_name:
                    print(f"Camera '{camera_name}' is already parented to '{group_name}', skipping parent operation.")
                else:
                    cmds.parent(camera_name, group_name)  # 부모가 다르면 페어런트
                    print(f"Camera '{camera_name}' was parented to existing group '{group_name}'.")
            else:
                cmds.group(camera_name, name=group_name)  # 새로운 그룹 생성
                print(f"New group '{group_name}' was created with camera '{camera_name}'.")

        return camera_name

    @staticmethod
    def reference_file(file_path, group_name):
        """
        특정 파일이 존재하면 해당 파일을 Maya에 참조하는 함수.
        :param file_path: 참조할 파일의 경로
        :param group_name: 참조할 그룹의 이름
        """
        if os.path.exists(file_path):
            cmds.file(file_path, reference=True)
            print(f"The {group_name} file '{file_path}' was referenced.")
            
            # 그룹 내의 모든 오브젝트를 찾기
            # cmds.ls()는 부모를 기준으로 하여 오브젝트를 반환
            objects = cmds.ls(group=group_name, long=True)  # 이 줄을 제거하고 다음과 같이 수정
            if not objects:
                # 'parent' 플래그를 사용하여 오브젝트 찾기
                objects = cmds.listRelatives(group_name, children=True, type="transform")
            
            if objects:
                return objects  # 객체 이름들의 리스트를 리턴
            else:
                print(f"No objects found in the group '{group_name}'.")
                return []
        else:
            print(f"The {group_name} file '{file_path}' was not found.")
            return []
        
    @staticmethod
    def lock_transform(object_names):
        """주어진 오브젝트들의 트랜스폼 속성을 락 설정"""
        if object_names:
            for obj_name in object_names:
                # 각 오브젝트의 트랜스폼 속성 락
                cmds.setAttr(f"{obj_name}.translateX", lock=True)
                cmds.setAttr(f"{obj_name}.translateY", lock=True)
                cmds.setAttr(f"{obj_name}.translateZ", lock=True)
                cmds.setAttr(f"{obj_name}.rotateX", lock=True)
                cmds.setAttr(f"{obj_name}.rotateY", lock=True)
                cmds.setAttr(f"{obj_name}.rotateZ", lock=True)
                cmds.setAttr(f"{obj_name}.scaleX", lock=True)
                cmds.setAttr(f"{obj_name}.scaleY", lock=True)
                cmds.setAttr(f"{obj_name}.scaleZ", lock=True)
                cmds.setAttr(f"{obj_name}.visibility", lock=True)

                # shapes 잠그기
                cmds.setAttr(f"{obj_name}.horizontalFilmAperture", lock=True)
                cmds.setAttr(f"{obj_name}.verticalFilmAperture", lock=True)
                cmds.setAttr(f"{obj_name}.focalLength", lock=True)
                cmds.setAttr(f"{obj_name}.lensSqueezeRatio", lock=True)
                cmds.setAttr(f"{obj_name}.fStop", lock=True)
                cmds.setAttr(f"{obj_name}.focusDistance", lock=True)
                cmds.setAttr(f"{obj_name}.shutterAngle", lock=True)
                cmds.setAttr(f"{obj_name}.centerOfInterest", lock=True)
                cmds.setAttr(f"{obj_name}.locatorScale", lock=True)
                print(f"The object '{obj_name}' was locked.")
        else:
            print("No valid objects found to lock.")

    @staticmethod
    def validate_hierarchy(group_name, child_list=None, exception_group=None):
        """
        특정 그룹과 자식 객체들이 존재하는지 확인하는 함수.
        :param group_name: 부모 그룹 이름
        :param child_list: 확인할 자식 그룹들의 이름들 (가변 인자)
        :param exception_groups: 자식이 없어도 통과할 그룹 리스트
        :return: 그룹이 존재하고, 자식 그룹들이 모두 존재하면 True, 아니면 False
        """
        # valid_list가 None이면 빈 리스트로 설정
        if not child_list:
            child_list = []

        if exception_group is None:
            exception_group = set()  # None이면 빈 set으로 초기화
            
        # 그룹 존재 여부 확인
        if not cmds.objExists(group_name):
            print(f"Validation failed: Group '{group_name}' does not exist.")
            return False

        if group_name in exception_group:
            print(f"Validation passed: Group '{group_name}' exists (empty check skipped).")
            return True
        
        # child_list가 있을 경우에만 자식 객체들 확인
        if child_list:
            existing_children = cmds.listRelatives(group_name, children=True, fullPath=False) or []
            for child in child_list:
                if child not in existing_children:
                    print(f"Validation failed: '{child}' does not exist under group '{group_name}'.")
                    return False
            # child_list에 있는 자식들이 모두 존재하면 True
            print(f"Validation passed: All children in child_list exist under group '{group_name}'.")
            return True

        # child_list가 비어있을 경우 자식 객체 존재 여부 확인
        existing_children = cmds.listRelatives(group_name, children=True, fullPath=False) or []
        if not existing_children:
            print(f"Validation failed: Group '{group_name}' exists but is empty.")
            return False

        # 자식 객체가 존재하면 True
        print(f"Validation passed: Group '{group_name}' exists and has children.")
        return True

    @staticmethod
    def validate_anim_curve():
        """animCurveTL 노드가 존재하는지 확인하는 함수"""
        if not bool(cmds.ls(type="animCurveTL")):
            print("Validation failed: 'animCurveTL' node does not exist.")
            return False
        else:
            print("Validation passed: 'animCurveTL' node exists.")
            return True

    @staticmethod
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

