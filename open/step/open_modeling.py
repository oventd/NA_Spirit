import maya.mel as mel
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import MayaUtils

class ModelingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print ("Opening modeling step")

    class Open:
        @staticmethod
        def setup(geo_group_name="geo"):
            MayaUtils.create_group(geo_group_name)
            MayaUtils.create_group("Low", parent = "geo")
            MayaUtils.create_group("High", parent = "geo")

    class Publish:
        @staticmethod
        def validate(geo_group_name="geo", child_list = ["Low", "High"]):
            
            if MayaUtils.validate_hierarchy(geo_group_name):
                print(f"Validation passed:'{geo_group_name}' exists.")
            else:
                print(f"Validation failed:'{geo_group_name}' does not exist.")

            if MayaUtils.validate_hierarchy(geo_group_name, child_list):
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재합니다.")
            else:
                print("Geo 그룹 하위에 Low와 High 그룹이 모두 존재하지 않습니다.")

        @staticmethod
        def publish(geo_group_name="geo", export_path="/home/rapa/maya_pub/modeling"):
            """ 특정 그룹을 USD와 MB 파일로 export """
            
            # geo 그룹이 존재하는지 확인
            if not cmds.objExists(geo_group_name):
                print(f"Error: Group '{geo_group_name}' does not exist.")
                return False
            
            # MB 파일 내보내기
            mb_export_path = os.path.splitext(export_path)[0] + ".mb"
            if not MayaUtils.file_save(mb_export_path, file_format="mb"):
                return False
            
            # USD Export 옵션 설정
            export_options = ";".join([
                "defaultUSDFormat=usdc",  # ✅ 바이너리 포맷을 맨 앞에 배치
                "shd=none",               # 쉐이딩 데이터 없음
                "mt=0",                   # 머티리얼 포함 안 함
                "vis=1",                  # 가시성 유지
                "uvs=1"                   # UV 포함
            ])
            
            # USD 파일 내보내기
            usd_export_path = os.path.splitext(export_path)[0] + ".usdc"
            usd_export_options = ";".join([
                "defaultUSDFormat=usdc",  # 바이너리 포맷
                "shd=none",               # 쉐이딩 데이터 없음
                "mt=1",                   # 머티리얼 포함
                "vis=0",                  # 가시성 비활성화
                "uvs=1"                   # UV 포함
            ])
            if not MayaUtils.file_save(usd_export_path, file_format="usd", export_options=usd_export_options):
                return False
            
            print(f"Modeling publish completed for {geo_group_name}.")
            return True
   
if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup()
    ModelingStep.Publish.validate()
    ModelingStep.Publish.publish()
    