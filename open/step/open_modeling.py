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
            
            if not MayaUtils.validate_hierarchy(geo_group_name):
                print(f"Validation failed: '{geo_group_name}' does not exist.")
                return False
             
            # 하위 그룹 검증
            if not MayaUtils.validate_hierarchy(geo_group_name, child_list):
                print("Validation failed: Geo 그룹 하위에 Low와 High 그룹이 존재하지 않습니다.")
                return False

            print("Validation passed: 모든 조건을 충족합니다.")
            return True  

        @staticmethod
        def publish(geo_group_name="geo", entity_path="", step=""):
            """ 특정 그룹을 USD와 MB 파일로 export """
            
            if not ModelingStep.Publish.validate(geo_group_name):  # validate 호출 시 geo_group_name 전달
                print("Publish aborted: Validation failed.")
                return False  # 검증 실패 시 퍼블리싱 중단
        
            if not export_path:
                print("Error: No export path provided.")
                return False
            
            # export_path 계산
            get_usd_export_path = SgPathUtils.get_usd_publish_dir(entity_path, step)
            export_path = SgPathUtils.get_usd_publish_dir(entity_path, step)

            publish_settings = StepOpenMaya.Publish.get_publish_settings()
            render_settings = StepOpenMaya.Publish.get_render_settings()

            # publish_settings 설정에 따른 처리
            if not publish_settings["modeling"]["geo"]["all"]:  # all이 False일 경우 자식 모두 가져오기
                children = MayaUtils.all_false(geo_group_name)
                print(f"Importing all children of {geo_group_name} at once.")
            else:  # all이 True일 경우 자식 하나씩 가져오기
                children = MayaUtils.all_true(geo_group_name)
                print(f"Importing specific children of {geo_group_name}.")

            # isReferenced에 따른 처리
            if not publish_settings["modeling"]["geo"]["isReferenced"]:  # isReferenced가 False일 경우
                MayaUtils.isReferenced_false()  # 레퍼런스가 없는 경우의 처리
            else:  # isReferenced가 True일 경우
                MayaUtils.isReferenced_true()  # 레퍼런스가 있는 경우의 처리

            """ 파일 내보내는 파트"""
            # MB 파일 내보내기
            mb_export_path = os.path.splitext(export_path)[0] + ".mb"
            if not MayaUtils.file_export(mb_export_path, file_format="mb"):
                return False
            
            # USD 파일 내보내기
            usd_export_path = os.path.splitext(export_path)[0]
            usd_export_options = render_settings.get("modeling", {}).get("geo", {}).get("usd_export_options", [])
            if usd_export_options:
                usd_export_options = ";".join(usd_export_options)
            else:
                usd_export_options = ""  # 값이 없다면 빈 문자열로 대체

            if not MayaUtils.file_export(usd_export_path, file_format="usd", export_options=usd_export_options):
                return False
            
            print(f"Modeling publish completed for {geo_group_name}.")
            return True


if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup()
    ModelingStep.Publish.validate()
    ModelingStep.Publish.publish()
    