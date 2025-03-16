import os
import sys

utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../")) + "/utils"
sys.path.append(utils_dir)

from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils


class PublishUsdProcessor:
    def __init__(self, session_path: str):
        self.session_path = session_path
        self.entity_path = SgPathUtils.trim_entity_path(session_path)
        self.entity_name = os.path.basename(self.entity_path)
        self.entity_usd_path = os.path.join(self.entity_path, self.entity_name,".usd")
    
        self.step = SgPathUtils.get_step_from_path(session_path)
        
        self.open_setup(self)

        self.entity_type = SgPathUtils.get_entity_type(self.entity_path)
        self.publish_dir = os.path.join(self.entity_path, "publish")

        

        self.step_publish_data_dict = {
            MODELING: ["geo"],
            RIGGING: [],
            MATCHMOVE: ["camera", "Asset"],
            LAYOUT: ["camera", "Asset"],
            ANIMATING: ["camera", "anim_cache"],
            LIGHTING: ["light"],
        }
        self.step_usd_dict = {}

        # Step을 문자열로 선언하여 객체를 동적으로 불러올 수 있도록 변경
        self.step_class_mapping = {
            MODELING: "Model",
            RIGGING: "Rig",
            MATCHMOVE: "Matchmove",
            LAYOUT: "Layout",
            ANIMATING: "Animating",
            LIGHTING: "Light",
        }

    @staticmethod
    def get_arg_dict(geo=None, char=None, anim_cache=None, terrain=None, camera=None, light=None):
        return {
            "geo": geo,
            "char": char,
            "anim_cache": anim_cache,
            "terrain": terrain,
            "camera": camera,
            "light": light,
        }

    def validate_args(self, step, provided_args):
        """ 단계별 필수 데이터를 검증하는 함수 """
        if step not in self.step_publish_data_dict:
            raise ValueError(f"Invalid step: {step}")

        required_keys = self.step_publish_data_dict.get(step, [])
        un_provided_keys = [arg for arg in required_keys if provided_args.get(arg) is None]

        if un_provided_keys:
            raise ValueError(f"Required keys not provided: {un_provided_keys}")

    def open_setup(self):
        """ 각 Step에 대한 USD 파일을 생성하는 함수 """
        self.entity_usd = os.path.join(self.entity_path, f"{self.entity_name}.usda")
        UsdUtils.create_usd_file(self.entity_usd)

        step_usd = os.path.join(self.publish_dir, self.step, f"{self.entity_name}_{self.step}.usda")
        UsdUtils.create_usd_file(step_usd)

        self.step_usd_dict[self.step] = step_usd

    def process(self, step, provided_args):
        """ 클래스 이름을 문자열로 저장하고, getattr()을 사용해 동적으로 로드 """
        self.validate_args(step, provided_args)

        class_name = self.step_class_mapping.get(step)
        if not class_name:
            raise ValueError(f"Unsupported step: {step}")

        # 올바르게 getattr을 호출해야 함 (self가 아니라 클래스에서 가져옴)
        step_class = getattr(PublishUsdProcessor, class_name, None)
        if not step_class:
            raise ValueError(f"Step class {class_name} not found in {self.__class__.__name__}")

        # 동적으로 클래스 인스턴스 생성 후 실행
        processor = step_class(self)
        processor.process(**provided_args)

    # 내부 클래스들 정의
    class Model:
        def __init__(self, parent):
            self.parent = parent

        def process(self, geo=None, **kwargs):
            print(f"Processing Model step with geo: {geo}")
            if geo:
                UsdUtils.add_sublayer(self.parent.entity_usd, geo)

    class Rig:
        def __init__(self, parent):
            self.parent = parent

        def process(self):
            print("Processing Rig step")

    class Matchmove:
        def __init__(self, parent):
            self.parent = parent

        def process(self, camera=None, terrain=None, **kwargs):
            print(f"Processing Matchmove step with camera: {camera}, terrain: {terrain}")
            if camera:
                UsdUtils.add_sublayer(self.parent.entity_usd, camera)
            if terrain:
                UsdUtils.add_sublayer(self.parent.entity_usd, terrain)

    class Layout:
        def __init__(self, parent):
            self.parent = parent

        def process(self, assets_path=None, camera=None, **kwargs):
            print(f"Processing Layout step with assets_path: {assets_path}, camera: {camera}")
            if camera:
                UsdUtils.add_sublayer(self.parent.entity_usd, camera)

    class Animating:
        def __init__(self, parent):
            self.parent = parent

        def process(self, anim_cache=None, camera=None, **kwargs):
            print(f"Processing Animating step with anim_cache: {anim_cache}, camera: {camera}")
            if camera:
                UsdUtils.add_sublayer(self.parent.entity_usd, camera)
            if anim_cache:
                UsdUtils.add_sublayer(self.parent.entity_usd, anim_cache)

    class Light:
        def __init__(self, parent):
            self.parent = parent

        def process(self, light=None, **kwargs):
            print(f"Processing Lighting step with light: {light}")
            if light:
                UsdUtils.add_sublayer(self.parent.entity_usd, light)


if __name__ == "__main__":
    root1_path = "/nas/sam/show/applestore/assets/Character/Bille"

    processor = PublishUsdProcessor(root1_path)
    processor.process(MODELING, {"geo": "/path/to/geo.usda"})
    processor.process(MATCHMOVE, {"camera": "/path/to/camera.usda", "terrain": "/path/to/terrain.usda"})
