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

def open_ref_file(file_path):
    file_path = r'D:\NA_Spirit_assets\apple_box\RIG\work\maya\apple_box_RIG.v003.ma'
    cmds.file(file_path, 
            force=True,  # 변경 사항 무시하고 강제 오픈
            open=True, 
            ignoreVersion=True,  # 버전 차이 무시
            prompt=False,  # 경고창 띄우지 않음
            loadReferenceDepth="all")  # Reference 모두 로드


def replace_reference_paths(input1, input2):
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

# 사용 예시
input1 = "/nas/spirit/project/spirit/assets/Prop/"  # 기존 경로 패턴
input2 = "D:/NA_Spirit_assets/"  # 변경할 새로운 경로

replace_reference_paths(input1, input2)
