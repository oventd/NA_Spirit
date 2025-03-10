from shotgun_api3 import Shotgun
import os

# ShotGrid 서버 정보 입력

SERVER_PATH = "https://hi.shotgrid.autodesk.com"  # 실제 ShotGrid 서버 주소
SCRIPT_NAME = "nayeon_key"  # ShotGrid 관리자에게 받은 스크립트 이름
API_KEY = "syeswcrleslhjbh4bd!poRvde"  # ShotGrid 관리자에게 받은 API 키

# ShotGrid API 연결
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)
PROJECT_ID = 124  # 실제 프로젝트 ID로 변경하세요

#https://hi.shotgrid.autodesk.com/page/5827#PublishedFile_54  << 참고 사이트



'''
자동요소 

Created by : 형민 박
Date Created : 02/28/25 09:54am
Date Updated : Today 05:20pm
Path Cache : spirit/assets/Character/Hero/MDL/publish/caches/scene.v001.abc
Description : No Value
Downstream Published Files : No Value
Id : 54
Link : Hero 
Local Path : No Value
Name : scene.abc
Path : scene.v001.abc
Path Cache Storage :Nas_Spirit
Project : Spirit
Published File Name : scene.v001.abc
Published File Type : No Value
Status : 
Tags : No Value
Task : Model 
Updated by : 나연 조
Upstream Published Files : scene.v001.ma 
Version : No Value
Version Number : 1

'''

"""
1. ShotGrid에서 기본적으로 자동 저장되는 데이터

Created by : 파일을 생성한 사용자 (ShotGrid가 자동 기록)
Date Created : 파일이 생성된 날짜 (ShotGrid가 자동 기록)
Date Updated : 파일이 마지막으로 업데이트된 날짜 (ShotGrid가 자동 기록)
Id : ShotGrid에서 부여하는 고유 ID (자동 생성)
Project : 해당 파일이 속한 프로젝트 (ShotGrid에서 자동 저장)
Updated by : 마지막으로 파일을 업데이트한 사용자 (ShotGrid가 자동 기록)
Version Number : 버전 관리 번호 (ShotGrid가 자동 부여)

2. 추가로 저장해야 하는 항목 (사용자가 입력해야 함)

Path Cache : ShotGrid 데이터베이스에 저장되는 파일의 경로 (자동으로 저장될 수도 있지만, 특정 경로를 강제 설정하려면 직접 추가해야 함)
Description : 파일에 대한 설명 (기본적으로 "No Value", 사용자가 직접 입력해야 함)
Downstream Published Files : 이 파일을 사용하는 후속 파일 목록 (자동 저장되지 않음, 사용자가 관리해야 함)
Link : 이 파일이 연결된 에셋, 샷, 혹은 Task 정보 (자동으로 채워질 수도 있지만, 명확한 링크를 원하면 입력 필요)
Local Path : ShotGrid 외부에서 사용되는 로컬 파일 경로 (필요하면 추가해야 함)
Name : ShotGrid 상에서 관리할 파일명 (일반적으로 자동 설정되지만, 특정 명칭을 부여하려면 추가해야 함)
Path Cache Storage : 파일이 저장된 스토리지 정보 (자동 설정될 수도 있지만, 명확한 정보 제공을 위해 추가해야 함)
Published File Name : ShotGrid에 업로드된 파일의 이름 (기본적으로 자동 생성되지만, 특정 규칙을 따르려면 추가해야 함)
Published File Type : 파일의 유형 (예: Alembic, EXR, Maya 등, 자동으로 설정되지 않으므로 직접 추가 필요)
Status : ShotGrid 내에서 파일의 현재 상태 (예: WIP, Final 등, 사용자가 설정해야 함)
Tags : 태그 정보 (자동 생성되지 않으며, 필요에 따라 추가 가능)
Task : 이 파일이 속한 작업(Task) 정보 (사용자가 수동으로 설정해야 함)
Upstream Published Files : 이 파일이 의존하는 상위 파일 목록 (자동 저장되지 않음, 사용자가 관리해야 함)
Version : ShotGrid에서 파일 버전을 자동 관리하지만, 특정 정보를 추가하려면 수동 입력해야 함  

3. 선택적으로 저장할 수 있는 항목 (입력하지 않아도 무방)

Description : 설명이 필요 없을 경우 비워도 무방
Tags : 특정 태그를 관리하지 않는 경우 생략 가능
Downstream Published Files : 후속 파일 관리가 필요 없는 경우 입력하지 않아도 됨
Upstream Published Files : 연관된 상위 파일이 없을 경우 생략 가능
Local Path : ShotGrid 내에서만 관리할 경우 필요 없음
Status : 파일 상태를 따로 관리하지 않는다면 입력하지 않아도 됨
Published File Type : ShotGrid에서 특정 유형이 필요하지 않다면 생략 가능

"""

###########################################################

# def published_file_info(PUBLISHED_FILE_ID,description=None, downstream_published_files=None, link=None, local_path, published_file_name, status, tags, task, upstream_published_files, version, version_number):

published_file = sg.find_one("PublishedFile", [["id", "is", 54]], ["id", "published_file_name", "path"])
path_cache_storage_data = published_file['path']["local_storage"]["name"]

#자동 생성과 수동 생성 항목의 추가 순서를 달리해서 자동으로 생성된 부분의 데이터를 가지고 노는 방법이 좋을듯
 






# published_filetype = {published_file['published_file_type']}

# print(published_filename)
 

#     local_path = "/mnt/storage/spirit/scene.v001.abc"
#     path = os.path.basename(local_path)
#     published_file_data = {
#     "name": "scene.abc",  # 파일 이름
#     "path_cache": "spirit/assets/Character/Hero/MDL/publish/caches/scene.v001.abc",  # 파일 경로  #샷그리드 내부의 주소 /// 자동 생성
#     "path_cache_storage": published_filetype  ###"Nas_Spirit",  # 저장소 정보
#     "description": "Final version of model",  # 설명
#     "downstream_published_files": [],  # 하위 의존 파일
#     "link": {"type": "Asset", "id": 301, "name": "Hero"},  # 연결된 Asset
#     "local_path": local_path,  # 로컬 경로
#     "path": path,  # 파일 경로 (파일명)    <<<받아와서 변경 
#     "published_file_name": published_filename,  # ShotGrid에 등록된 파일명  <<<받아와서 변경 
#     "published_file_type": published_filetype,   # 파일 유형 <<<받아와서 변경 
#     "status": "Ready",  # 상태
#     "tags": ["Modeling", "Cache"],  # 태그
#     "task": {"type": "Task", "id": 6219, "name": "Model"},  # 연결된 Task
#     "upstream_published_files": [{"type": "PublishedFile", "id": 50}],  # 상위 파일
#     "version": {"type": "Version", "id": 201},  # 연결된 Version
#     }


#     # ✅ None 값 제거 (ShotGrid에서 None을 허용하지 않는 필드를 자동 제거)
#     published_file_data = {k: v for k, v in published_file_data.items() if v is not None and v != []}

#     # ✅ ShotGrid에 Published File 생성
#     new_published_file = sg.create("PublishedFile", published_file_data)
#     print(f"✅ Published File created: {new_published_file['id']}")



# published_file_info(PUBLISHED_FILE_ID = 54,
#                     path_cache_storage="Nas_Spirit",
#                     description="움하하_엘런빅의 맛이 어때",
#                     link={"type": "Asset", "id": 301, "name": "Hero"}),
#                     local_path = "nas/spirit/assets/Character/Hero/MDL/publish/caches/scene.v001.abc",






# ✅ 파일 정보
file_path = "/mnt/storage/spirit/scene.v001.abc"

local_storage = sg.find_one("LocalStorage", [["code", "is", "Nas_Spirit"]], ["id"])

path = {
    "local_path": "/mnt/storage/spirit/scene.v001.abc",  # 실제 파일 경로
    "local_storage": {
        "type": "LocalStorage",
        "id": 2  # ShotGrid에서 조회한 LocalStorage ID
    }
}

 
default_version = 1  # 기본 버전 번호
task_id = 6219
ling = 301


local_storage = sg.find_one("LocalStorage", [["code", "is", "Nas_Spirit"]], ["id"])

if not local_storage:
    raise ValueError(" LocalStorage 'Nas_Spirit' not found in ShotGrid.")

local_storage_id = local_storage["id"]
print(f" Found LocalStorage: Nas_Spirit (ID: {local_storage_id})")

# ✅ 필수 데이터 확인 후 기본값 설정
published_file_data = {
    "name": os.path.basename(file_path),  # 파일명 자동 설정
    "path": file_path,  # 파일 경로
    "path_cache": "spirit/assets/Character/Hero/MDL/publish/caches/" + os.path.basename(file_path),  # ShotGrid 내부 경로
    "path_cache_storage": local_storage_id,  # 저장소 기본값 설정
    "published_file_type": "Alembic Cache",  # 기본 파일 유형
    "task": {"type": "Task", "id": 6219},  # Task ID (필수)
    "link": {"type": "Asset", "id": 301},  # 연결된 Asset (필수)
    "version_number": default_version,  # 기본 버전 설정
}














# ✅ ShotGrid에 Published File 생성
new_published_file = sg.create("PublishedFile", published_file_data)
PUBLISHED_FILE_ID = new_published_file["id"]
print(f"✅ Published File created: {PUBLISHED_FILE_ID}")


updated_published_file = sg.find_one("PublishedFile", [["id", "is", PUBLISHED_FILE_ID]], ["id", "name", "path_cache", "path_cache_storage"])

print(f"생성 후 조회: {updated_published_file['id']}")
print(f"Path Cache Storage: {updated_published_file.get('path_cache_storage', 'Not Assigned')}")
