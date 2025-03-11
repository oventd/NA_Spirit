from shotgun_api3 import Shotgun
import os
from shotgrid_client_config import get_shotgrid_client

sg = get_shotgrid_client()


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


# PUBLISHED_FILE_ID = 180  # 수정할 Published File ID

# updated_published_file = sg.update("PublishedFile", PUBLISHED_FILE_ID, {
#     "description": "음 설명을 추가해볼까요"}, {"name":"이름이라고 합니당"},{"sg_local_path":"/mnt/storage/spirit/scene.v001.abc"})

# print(f"✅ Updated Published File {PUBLISHED_FILE_ID} with new description.")




PUBLISHED_FILE_ID = 180  # 수정할 Published File ID

def update_published_file(published_file_data):
    updated_published_file = sg.update(
        "PublishedFile", 
        PUBLISHED_FILE_ID, published_file_data,  # 연결된 엔티티
        
    )

    print(f"✅ Updated Published File {PUBLISHED_FILE_ID} with new values.")


if __name__ == "__main__":
    
    description ="테스트중입니다."
    file_name = "파일이름입니다"
    local_path = "/mnt/storage/spirit/scene.v003.abc"
    cache_path = "spirit/assets/Character/Hero/MDL/publish/caches/scene.v003.abc"
    published_file_type_id = 1
    upstram_file_id = 100
    downstream_file_id = 101
    image_path = "/nas/spirit/DB/thum/3d_assets/thum001.png"
    asset_id= 1419
    


    published_file_data={

        "description": "테스트중입니다",
        "name": "파일이름입니다",
        "sg_local_path": "/mnt/storage/spirit/scene.v003.abc",  # 유효한 파일 경로
        "path_cache": "spirit/assets/Character/Hero/MDL/publish/caches/scene.v003.abc",  # 상대 경로
        "version_number": 2,  # 버전 번호 업데이트
        "published_file_type": {"type":"PublishedFileType", "id": 1},  # 유효한 파일 유형
        "upstream_published_files": [{"type": "PublishedFile", "id": 100}],  # 상위 PublishedFile ID 배열
        "downstream_published_files": [{"type": "PublishedFile", "id": 101}],  # 하위 PublishedFile ID 배열
        "image": "/nas/spirit/DB/thum/3d_assets/thum001.png",  # 이미지 경로
        "entity": {"type": "Asset", "id": 1419}
        }
    
    update_published_file(published_file_data)

