import os
import maya.cmds as cmds
import shutil
import sys
import re
import sgtk
sys.path.append('/home/rapa/NA_Spirit/utils')
from sg_path_utils import SgPathUtils
# file_path = 'D:/NA_Spirit_assets/apple_box\\MDL\\publish\\maya\\apple_box_MDL.v006.ma'

class DownloadReferencePathMatcher:
    def __init__(self,context):
        self.context = context
        self.project_dir = self.get_project_directory()
        self.asset_dir = os.path.join(self.project_dir, "assets")



    def get_project_directory(self) -> str:
        """
        현재 ShotGrid Toolkit 프로젝트의 루트 디렉토리를 반환.

        :return: 프로젝트 디렉토리 경로 (str)
        """
        if not self.context or not self.context.project:
            raise ValueError("현재 ShotGrid 프로젝트 컨텍스트를 찾을 수 없습니다.")

        # 프로젝트의 루트 디렉토리 가져오기
        tk = self.engine.sgtk
        return tk.project_path

    def open_maya_file_force(self,file_path):
        cmds.file(file_path, 
          force=True,  # 기존 씬 변경 내용 무시하고 강제 오픈
          open=True, 
          ignoreVersion=True,  # Maya 버전 차이 무시
          prompt=False,  # 경고 창 띄우지 않음
          loadReferenceDepth="none",  # 처음에는 reference를 불러오지 않음
          options="v=0")  # 추가적인 창이 뜨지 않도록 설정

    def find_files_by_extension(self,root_dir, extensions):
        """
        주어진 디렉터리에서 특정 확장자를 가진 파일을 재귀적으로 찾음.
        
        :param root_dir: 검색할 최상위 디렉터리
        :param extensions: 찾을 확장자 리스트
        :return: 해당 확장자의 파일 리스트
        """
        found_files = []
        for dirpath, _, filenames in os.walk(root_dir):
            for file in filenames:
                print
                if file.lower().endswith(extensions):
                    found_files.append(os.path.join(dirpath, file))
        return found_files


    def open_ref_file(self,file_path):
        cmds.file(file_path, 
                force=True,  # 변경 사항 무시하고 강제 오픈
                open=True, 
                ignoreVersion=True,  # 버전 차이 무시
                prompt=False,  # 경고창 띄우지 않음
                loadReferenceDepth="all")  # Reference 모두 로드


    def replace_reference_paths(self,input1, input2):
        """
        Maya 씬의 모든 reference 노드를 찾아 기존 경로를 input1에서 input2로 변경하여 기존 노드에 반영.

        :param input1: 기존 reference 경로에서 변경할 문자열
        :param input2: 변경된 새로운 문자열
        """
        # 현재 씬에서 모든 reference 가져오기
        references = cmds.file(q=True, reference=True) or []
        
        if not references:
            print("⚠️ Reference가 없습니다.")
            return
        
        modified_references = []  # 변경된 reference 목록 저장

        for ref in references:
            try:
                # 레퍼런스 노드 이름 가져오기
                reference_node = cmds.referenceQuery(ref, referenceNode=True)

                # 기존 reference의 실제 파일 경로 가져오기
                ref_path = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)

                # 새로운 경로 생성
                new_path = ref_path.replace(input1, input2)

                if ref_path != new_path:
                    print(f"🔄 변경됨: {ref_path} → {new_path}")

                    # 기존 reference 노드에 새로운 경로 반영
                    cmds.file(new_path, loadReference=reference_node, type="mayaAscii", options="v=0;")
                    
                    modified_references.append(new_path)
            
            except Exception as e:
                print(f"❌ Reference 변경 실패: {ref} | 오류: {e}")

        if modified_references:
            print("✅ 모든 reference가 성공적으로 업데이트되었습니다.")
        else:
            print("⚠️ 변경된 reference가 없습니다.")


    def copy_folder(self, source_folder: str, destination_folder: str):
        """
        특정 폴더를 대상 경로로 복사하는 메서드.

        :param source_folder: 원본 폴더 경로
        :param destination_folder: 복사할 대상 폴더 경로
        """
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"원본 폴더가 존재하지 않습니다: {source_folder}")

        if os.path.exists(destination_folder):
            shutil.rmtree(destination_folder)  # 기존 폴더 삭제

        try:
            shutil.copytree(source_folder, destination_folder)
            print(f"폴더 복사가 완료되었습니다: {source_folder} -> {destination_folder}")
        except Exception as e:
            print(f"폴더 복사 중 오류 발생: {e}")

    def replace_text_in_ascii_file(input_file, target_string, replacement_string):
        """
        Reads an ASCII file, replaces occurrences of target_string with replacement_string,
        and writes the modified content to a new file.

        :param input_file: Path to the input ASCII file.
        :param target_string: The string to be replaced.
        :param replacement_string: The string to replace with.
        """
        try:
            with open(input_file, 'r', encoding='ascii') as file:
                content = file.read()
            
            modified_content = content.replace(target_string, replacement_string)

            with open(input_file, 'w', encoding='ascii') as file:
                file.write(modified_content)

            print(f"Successfully replaced '{target_string}' with '{replacement_string}' in '{input_file}'.")

        except UnicodeDecodeError:
            print("Error: The file is not a valid ASCII file.")
        except FileNotFoundError:
            print("Error: The input file was not found.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def process(self,category, db_asset_dir):
        current_session = self.get_current_maya_scene_path()

        asset_name = os.path.dirname(db_asset_dir)
        project_asset_dir = os.path.join(self.project_dir, "assets", category, asset_name)

        # 검색할 디렉터리 경로 설정
        self.copy_folder(db_asset_dir, project_asset_dir)

        # ma, mb 파일 찾기
        self.replace_paths(project_asset_dir)

        rig_ma_publish_dir = os.path.join(project_asset_dir, "RIG", "publish", "maya")
        last_rig_ma = self.get_latest_version_file(rig_ma_publish_dir)

        self.open_maya_file_force(current_session)
        cmds.file(last_rig_ma, reference=True)


    def replace_paths(self, project_asset_dir):
        references = cmds.file(q=True, reference=True) or []
        if references:
            original_path = cmds.referenceQuery(references[0], filename=True, withoutCopyNumber=True)
        original_dir = SgPathUtils.trim_entity_path(original_path)[0]
        maya_files = self.find_files_by_extension(project_asset_dir, (".ma", ".mb"))
        # usd 파일 찾기
        usd_files = self.find_files_by_extension(project_asset_dir, ".usd")
        # 결과 출력
        print("Maya Files (.ma, .mb):", maya_files)
        print("USD Files (.usd):", usd_files)

        self.open_maya_file_force(maya_files[0])

        for maya_file in maya_files:
            self.open_maya_file_force(maya_file)
            self.replace_reference_paths(original_dir, project_asset_dir)

        for usd_file in usd_files:
            self.replace_text_in_ascii_file(usd_file, original_dir, project_asset_dir)

    
        
    def get_latest_version_file(self,folder_path):
        """
        주어진 폴더에서 '파일명.v###.ma' 형식의 파일 중 최신 버전의 파일을 반환

        :param folder_path: 검색할 폴더 경로
        :return: 최신 버전의 파일 전체 경로 또는 None
        """
        pattern = re.compile(r"^(.*)\.v(\d{3})\.ma$")  # 정규식 패턴 (모든 베이스 이름 지원)

        latest_version = -1
        latest_file = None

        for file in os.listdir(folder_path):
            match = pattern.match(file)
            if match:
                base_name, version = match.groups()  # 파일명과 버전 추출
                version = int(version)  # 버전 번호를 정수 변환

                if version > latest_version:
                    latest_version = version
                    latest_file = file

        if latest_file:
            return os.path.join(folder_path, latest_file)
        else:
            return None

    def get_current_maya_scene_path(self):
        """
        현재 열린 Maya 씬의 전체 파일 경로를 반환합니다.
        씬이 저장되지 않았다면 'untitled'를 반환합니다.
        """
        scene_path = cmds.file(q=True, sceneName=True)

        if not scene_path:
            print("⚠️ 현재 씬은 저장되지 않았습니다. (untitled)")
            return None
        
        print(f"📌 현재 씬 경로: {scene_path}")
        return scene_path