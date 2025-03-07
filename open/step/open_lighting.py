import maya.mel as mel
import maya.cmds as cmds
import os
import sys

sys.path.append('/home/rapa/NA_Spirit/open/step')
from step_open_maya import StepOpenMaya

sys.path.append('/home/rapa/NA_Spirit/utils')
from maya_utils import create_group,reference_file, create_usd_proxy, create_lighting_group  # 유틸 함수 임포트


class Lighting(StepOpenMaya):
    @staticmethod
    def __init__(self, env_usd):
        super().__init__()
        print("Opening lighting step")
        self.env_usd = env_usd
        # light 그룹 생성
        self.create_lighting_group()

    class Open:
        @staticmethod
        def setup(env_usd):
            print("Opening lighting step")

            # 라이트 그룹 생성
            create_group("light")

            # USD 로드
            create_usd_proxy("lighting")

            # env USD 파일이 존재하는지 확인 후 레퍼런스
            if not os.path.exists(env_usd):
                cmds.warning(f"Environment USD file not found: {env_usd}")
            else:
                reference_file(env_usd, "environment")

            # USD Layer Editor 실행 전 플러그인 확인
            if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
                cmds.loadPlugin("mayaUsdPlugin")

            cmds.mayaUsdLayerEditorWindow()
            print("Opened USD Layer Editor")

    class Publish:
        @staticmethod
        def validate():
            print("Validating Lighting setup...")
            # 여기에 검증 로직 추가 가능
            pass


if __name__ == "__main__":
    env_usd = "/home/rapa/3D_usd/Kitchen_set/assets/WallOrange/WallOrange.usd"

    lighting = Lighting(env_usd)
    Lighting.Open.setup(env_usd)  # 내부 클래스 방식으로 호출
    Lighting.Publish.validate()  # 검증 기능 호출
