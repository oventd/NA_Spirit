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
        def publish(geo_group_name="geo", export_path="/home/rapa/maya_pub/modeling/modeling"):
            """ 특정 그룹을 USD와 MB 파일로 export """
            
            if not export_path:
                print("Error: No export path provided.")
                return False

            publish_settings = StepOpenMaya.Publish.get_publish_settings()
            render_settings = StepOpenMaya.Publish.get_render_settings()

            # Publish 설정에 따른 처리
            if publish_settings["modeling"]["geo"]["all"]:
                print(f"Importing all children of {geo_group_name} at once.")
            else:
                print(f"Importing specific children of {geo_group_name}.")
            
            if publish_settings["modeling"]["geo"]["isReferenced"] is False:
                print(f"Exporting as static {geo_group_name}.")

            # MB 파일 내보내기
            mb_export_path = os.path.splitext(export_path)[0] + ".mb"
            if not MayaUtils.file_export(mb_export_path, file_format="mb"):
                return False
            
            # USD 파일 내보내기
            usd_export_path = os.path.splitext(export_path)[0]

            # render_settings에서의 usd_export_options 사용 (초기화 없이 결합)
            usd_export_options = render_settings.get("modeling", {}).get("geo", {}).get("usd_export_options", [])
            usd_export_options = ";".join(usd_export_options) if usd_export_options else ""  # 옵션이 없으면 빈 문자열

            if not MayaUtils.file_export(usd_export_path, file_format="usd", export_options=usd_export_options):
                return False
            
            print(f"Modeling publish completed for {geo_group_name}.")
            return True


if __name__ == "__main__":
    modeling = ModelingStep()
    ModelingStep.Open.setup()
    ModelingStep.Publish.validate()
    ModelingStep.Publish.publish()
    