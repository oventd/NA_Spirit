from shotgun_api3 import Shotgun
import os
from shotgrid_client_config import get_shotgrid_client

sg = get_shotgrid_client()


PUBLISHED_FILE_ID = 180  # 수정할 Published File ID

def update_published_file(PUBLISHED_FILE_ID,published_file_data):
    updated_published_file = sg.update(
        "PublishedFile", 
        PUBLISHED_FILE_ID, published_file_data,  # 연결된 엔티티
        
    )

    return updated_published_file

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

