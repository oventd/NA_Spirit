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



def get_cut_in_out(SHOT_ID): 
    current_steps = sg.find(
            "Shot",
            [["id", "is",SHOT_ID]],
            ["sg_cut_in", "sg_cut_out"]


        )
    return current_steps