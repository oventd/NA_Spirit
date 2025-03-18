import os

# file_path = 'D:/NA_Spirit_assets/apple_box\\MDL\\publish\\maya\\apple_box_MDL.v006.ma'

# cmds.file(file_path, 
#           force=True,  # 기존 씬 변경 내용 무시하고 강제 오픈
#           open=True, 
#           ignoreVersion=True,  # Maya 버전 차이 무시
#           prompt=False,  # 경고 창 띄우지 않음
#           loadReferenceDepth="none",  # 처음에는 reference를 불러오지 않음
#           options="v=0")  # 추가적인 창이 뜨지 않도록 설정
def find_files_by_extension(root_dir, extensions):
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

# 검색할 디렉터리 경로 설정
root_directory = "D:/NA_Spirit_assets/apple_box"  # 원하는 경로로 변경

# ma, mb 파일 찾기
maya_files = find_files_by_extension(root_directory, (".ma", ".mb"))

# usd 파일 찾기
usd_files = find_files_by_extension(root_directory, ".usd")

# 결과 출력
print("Maya Files (.ma, .mb):", maya_files)
print("USD Files (.usd):", usd_files)
file_path = r'D:\NA_Spirit_assets\apple_box\RIG\work\maya\apple_box_RIG.v003.ma'
cmds.file(file_path, 
          force=True,  # 변경 사항 무시하고 강제 오픈
          open=True, 
          ignoreVersion=True,  # 버전 차이 무시
          prompt=False,  # 경고창 띄우지 않음
          loadReferenceDepth="all")  # Reference 모두 로드

          
import maya.cmds as cmds

def get_all_references():
    """
    현재 열린 Maya 씬에서 모든 reference 파일 경로를 찾아 리스트로 반환.
    """
    reference_list = []
    
    # 현재 씬의 모든 reference 가져오기
    references = cmds.ls(type="reference")
    
    for ref in references:
        # 시스템 reference인지 확인 (파일 reference만 필터링)
        if cmds.referenceQuery(ref, isNodeReferenced=True):
            continue  # reference 내부의 reference 노드는 제외

        # reference 파일 경로 가져오기
        ref_file = cmds.referenceQuery(ref, filename=True, withoutCopyNumber=True)
        
        if ref_file and ref_file not in reference_list:
            reference_list.append(ref_file)

    return reference_list

# 실행
all_references = get_all_references()
print("🔹 Maya Scene References:", all_references)
