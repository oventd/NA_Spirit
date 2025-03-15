from shotgun_api3 import Shotgun
import os

# ShotGrid 서버 정보 입력

SERVER_PATH = "https://hi.shotgrid.autodesk.com"  # 실제 ShotGrid 서버 주소
SCRIPT_NAME = "nayeon_key"  # ShotGrid 관리자에게 받은 스크립트 이름
API_KEY = "syeswcrleslhjbh4bd!poRvde"  # ShotGrid 관리자에게 받은 API 키

# ShotGrid API 연결
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)
PROJECT_ID = 124  # 실제 프로젝트 ID로 변경하세요

#https://hi.shotgrid.autodesk.com/page/5826  << 참고 사이트


# Shot 엔티티의 cut_in, cut_out 값을 설정

SHOT_ID = 1182  # 수정할 Shot ID
new_cut_in = 1001
new_cut_out = 1200

# updated_shot = sg.update(
#     "Shot", 
#     SHOT_ID, 
#     {
#         "sg_cut_in": new_cut_in,
#         "sg_cut_out": new_cut_out
#     }
# )

# shot_fields = sg.schema_field_read("Shot")  # 엔티티 이름을 지정

#cut_in, cut_out의 값을 가져오는 코드

current_steps = sg.find(
        "Shot",
        [["id", "is",1182]],
        ["sg_cut_in", "sg_cut_out"]


    )
print(current_steps)