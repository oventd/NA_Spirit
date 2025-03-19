import maya.mel as mel
import maya.cmds as cmds
import os
import sys
import sgtk
sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya
sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import MayaUtils


class LightingStep(StepOpenMaya):
    def __init__(self):
        super().__init__()
        print("Opening lighting step")



    class Open(StepOpenMaya.Open):
        @staticmethod
        def setup( task_id=None, file_format=None):
            # 라이트 그룹 생성
            context = sgtk.current_engine().context
            project_path = context.project.path
            category = context.entity["type"]
            entity = context.entity["name"]
            usd_path = os.path.join(project_path,"squences" ,category, entity, f"{entity}.usd")
            MayaUtils.create_usd_proxy(usd_path)

            # # USD 로드
            # MayaUtils.create_usd_proxy("lighting") 

            # # env USD 파일이 존재하는지 확인 후 레퍼런스
            # if not os.path.exists(env_usd):
            #     cmds.warning(f"Environment USD file not found: {env_usd}")
            # else:
            #     MayaUtils.reference_file(env_usd, "environment")

            # # USD Layer Editor 실행 전 플러그인 확인
            # if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            #     cmds.loadPlugin("mayaUsdPlugin")

            # cmds.mayaUsdLayerEditorWindow()
            # print("Opened USD Layer Editor")

        @staticmethod    
        def reference(self):
            pass

    class Publish(StepOpenMaya.Publish):
        @staticmethod
        def validate():
            print("Validating Lighting setup...")
            # 여기에 검증 로직 추가 가능
            pass

        @staticmethod
        def publish(session_path: str,context ):
            """ 특정 그룹을 USD와 MB 파일로 export """
            StepOpenMaya.Publish.publish(session_path,context)

if __name__ == "__main__":
    env_usd = "/home/rapa/3D_usd/Kitchen_set/assets/WallOrange/WallOrange.usd"

    lighting = Lighting(env_usd)
    Lighting.Open.setup(env_usd)  # 내부 클래스 방식으로 호출
    Lighting.Publish.validate()  # 검증 기능 호출
