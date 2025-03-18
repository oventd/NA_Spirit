#프린트 형식
# ['67bd6ea2e63d06c897d0de1d', '67bd6ec57dbd058b9f0d9997', '67bd6ec57dbd058b9f0d999b']이 레퍼런스로 다운로드되었습니다
# ['67bd6ea2e63d06c897d0de1d']에셋이 임포트로 다운되었습니다



import os
import sys
sys.path.append('/home/rapa/NA_Spirit/utils/')
sys.path.append('/home/rapa/NA_Spirit/gui/')
from flow_utils import FlowUtils
from assetmanager import AssetService
from shotgun_api3 import Shotgun
from constant import SERVER_PATH, SCRIPT_NAME, API_KEY



class FlowUtils:

    def __init__(self):
        self.sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)
        asset_list = ['67bd6ea2e63d06c897d0de1d', '67bd6ec57dbd058b9f0d9997', '67bd6ec57dbd058b9f0d999b']
        self.redata_for_flow(asset_list)  #  객체 생성 시 자동 실행

    def get_asset_data(self, asset_list):
        asset_all_info = AssetService.get_assets_by_ids_all_return(asset_list)
        return asset_all_info
    
    def add_asset_project(self, project_id, code, discription, sg_asset_type):
        new_asset_data = {
            "project": {"type": "Project", "id": project_id},
            "code": code,
            "description": discription,
            "sg_asset_type":  sg_asset_type,
            "sg_status_list": "fin",
            # "created_by": {"type": "HumanUser", "id": 123}, #사원 등록 필요함
        }
        self.sg.create("Asset", new_asset_data)  #  인스턴스 변수 사용

    def redata_for_flow(self,asset_list):
        
        info_all = self.get_asset_data(asset_list)
        for info in info_all:
            code = info["name"]
            discription = info["description"]
            sg_asset_type = info["category"]
            self.add_asset_project(127, code, discription, sg_asset_type)  #127은 나중에 project id와 교체해주세용

        
       

flow_instance = FlowUtils()