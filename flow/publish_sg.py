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


#Published File Info
Created by : 형민 박
Date Created : 02/28/25 09:54am
Date Updated : Today 05:20pm
Description : No Value
Downstream Published Files : No Value
Id : 54
Link : Hero 
Local Path : No Value
Name : scene.abc
Path : scene.v001.abc
Path Cache : spirit/assets/Character/Hero/MDL/publish/caches/scene.v001.abc
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