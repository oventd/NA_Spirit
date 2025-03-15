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

    @staticmethod
    def file_export(file_path, export_options=None):
        """
        파일을 지정된 포맷으로 저장하는 함수.
        :param file_path: 저장할 파일의 경로
        :param file_format: 저장할 파일 포맷 (기본값: mayaBinary)
        :param export_options: 포맷에 해당하는 추가 옵션 (기본값: None)
        """
        _, ext = os.path.splitext(file_path)

        if ext == ".mb":
            return cmds.file(file_path, force=True, type="mayaBinary", exportSelected=True) # 호출 방식 확인
        
        elif ext == ".ma":
            return cmds.file(file_path, force=True, type="mayaAscii", exportSelected=True) # 호출 방식 확인
        
        elif ext == ".usd":       
            return cmds.file(file_path, force=True, options=export_options, type="USD Export", exportSelected=True)  # 호출 방식 확인
        else:
            print(f"Error: Unsupported file format {ext}")
            return False

    @staticmethod
    def export_maya_binary(file_path):
        """Maya Binary 형식으로 파일을 저장하는 함수."""
        
        print(f"Export {file_path} as Maya Binary.")
        return True

    @staticmethod
    def export_maya_ascii(file_path):
        """Maya ASCII 형식으로 파일을 저장하는 함수."""
        cmds.file(file_path, force=True, type="mayaAscii", exportSelected=True)
        print(f"Export {file_path} as Maya ASCII.")
        return True

    @staticmethod
    def export_usd(file_path, export_options=None):
        """USD 형식으로 파일을 저장하는 함수."""
        if export_options is None:
            export_options = ""
            print("Error: No export options provided for USD.")
        cmds.file(file_path, force=True, options=export_options, type="USD Export", exportSelected=True)
        print(f"Export {file_path} as USD.")
        return True
    



    """ 없어도 될 친구들"""
    @staticmethod
    def all_false(group_name):
        """all = false 시 나오는 메서드 (그룹의 자식 모두 반환)"""
        children = cmds.listRelatives(group_name, children=True) or []
        if not children:
            print(f"No children found in group '{group_name}'.")
        return children

    @staticmethod
    def all_true(group_name):
        """all = true 시 나오는 메서드 (각 자식 반환)"""
        children = cmds.listRelatives(group_name, children=False) or []
        if not children:
            print(f"No children found in group '{group_name}'.")
        return children
    
    def isReferenced_false():
        """isReferenced: false 시 나오는 메서드"""
        print("No referenced objects found. Proceeding with non-referenced objects.")

    def isReferenced_true(file_path, group_name):
        """isReferenced: true 시 나오는 메서드"""
        return MayaUtils.reference_file(file_path, group_name)


"""exportUVs=1;                 # UV 좌표 내보내기 (1=활성화, 0=비활성화)
        exportSkels=none;              # 스켈레톤 내보내기 옵션 (none, auto, explicit)
        exportSkin=none;               # 스킨 데이터 포함 여부 (none, auto, explicit)
        exportBlendShapes=0;           # 블렌드쉐이프 내보내기 (0=비활성화, 1=활성화)
        exportDisplayColor=0;          # Display Color 내보내기 (0=비활성화, 1=활성화)
        filterTypes=nurbsCurve;        # 내보낼 객체 유형 필터 (여기서는 NurbsCurve만 포함)
        exportColorSets=0;             # 컬러 세트 포함 여부 (0=비활성화, 1=활성화)
        exportComponentTags=0;         # 컴포넌트 태그 내보내기 여부 (0=비활성화, 1=활성화)
        defaultMeshScheme=catmullClark;# 기본 메시 스킴 (catmullClark, none, bilateral 등)
        animation=0;                   # 애니메이션 내보내기 (0=비활성화, 1=활성화)
        eulerFilter=0;                 # 오일러 필터 적용 여부 (0=비활성화, 1=활성화)
        staticSingleSample=0;          # 정적 프레임 샘플링 (0=비활성화, 1=활성화)
        startTime=1;                    # 내보내기 시작 프레임
        endTime=1;                      # 내보내기 종료 프레임
        frameStride=1;                  # 프레임 간격
        frameSample=0.0;                # 프레임 샘플링 간격
        defaultUSDFormat=usda;         # 기본 USD 포맷 (usda=텍스트, usdc=바이너리, usdz=압축)
        rootPrim=;                     # 루트 Prim 설정 (기본값: 없음)
        rootPrimType=scope;            # 루트 Prim 타입 설정 (scope, xform 등)
        defaultPrim=geo;               # 기본 Prim 지정
        exportMaterials=0;             # 머티리얼 내보내기 여부 (0=비활성화, 1=활성화)
        shadingMode=useRegistry;       # 쉐이딩 모드 (useRegistry, none, displayColor 등)
        convertMaterialsTo=[UsdPreviewSurface]; # 변환할 머티리얼 유형
        exportAssignedMaterials=1;     # 할당된 머티리얼 내보내기 여부 (0=비활성화, 1=활성화)
        exportRelativeTextures=automatic; # 상대 텍스처 경로 변환 여부 (automatic, absolute 등)
        exportInstances=1;             # 인스턴스 내보내기 (0=비활성화, 1=활성화)
        exportVisibility=0;            # 가시성 내보내기 (0=비활성화, 1=활성화)
        mergeTransformAndShape=0;      # Transform과 Shape 병합 여부 (0=비활성화, 1=활성화)
        includeEmptyTransforms=0;      # 빈 Transform 포함 여부 (0=비활성화, 1=활성화)
        stripNamespaces=1;             # 네임스페이스 제거 (0=비활성화, 1=활성화)
        worldspace=0;                  # 월드 공간 변환 여부 (0=비활성화, 1=활성화)
        exportStagesAsRefs=0;          # USD 스테이지를 참조로 내보낼지 여부 (0=비활성화, 1=활성화)
        excludeExportTypes=[Cameras,Lights]; # 내보내지 않을 객체 유형 (카메라, 라이트 제외)
        legacyMaterialScope=0"""      # 레거시 머티리얼 스코프 사용 여부 (0=비활성화, 1=활성화)