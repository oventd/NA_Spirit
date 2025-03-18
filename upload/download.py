import os

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
