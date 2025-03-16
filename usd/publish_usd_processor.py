import os
import sys

utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../")) + '/utils'
sys.path.append(utils_dir)

from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils


class PublishUsdProcessor:
    def __init__(self, entity_path: str):
        self.entity_path = SgPathUtils.trim_entity_path(entity_path)
        self.entity_name = os.path.basename(entity_path)
        self.entity_usd_path = ""

        self.entity_type = SgPathUtils.get_entity_type(entity_path)
        self.publish_dir = os.path.join(self.entity_path, "publish")

        self.step_publish_data_dict = {
            MODELING: ['geo'],
            RIGGING: [],
            MATCHMOVE: ["camera", "terrain"],
            LAYOUT: ["camera", "terrain"],
            ANIMATING: ["camera", "terrain", "anim_cache"],
            LIGHTING: ["light"],
        }
        self.step_usd_dict = {}

        # Step을 문자열로 선언하여 객체를 동적으로 불러올 수 있도록 변경
        self.step_class_mapping = {
            MODELING: "ModelStepUsdProcessor",
            RIGGING: "RigStepUsdProcessor",
            MATCHMOVE: "MatchmoveStepUsdProcessor",
            LAYOUT: "LayoutStepUsdProcessor",
            ANIMATING: "AnimatingStepUsdProcessor",
            LIGHTING: "LightingStepUsdProcessor"
        }

    @staticmethod
    def get_arg_dict(
        geo=None,
        char=None,
        anim_cache=None,
        terrain=None,
        camera=None,
        light=None
    ):
        return {
            "geo": geo,
            "char": char,
            "anim_cache": anim_cache,
            "terrain": terrain,
            "camera": camera,
            "light": light
        }

    def validate_args(self, step, provided_args):
        if self.step_publish_data_dict.get(step) is None:
            raise ValueError(f"Invalid step: {step}")

        required_keys = self.step_publish_data_dict.get(step, [])
        un_provided_keys = [arg for arg in required_keys if provided_args.get(arg) is None]

        if un_provided_keys:
            raise ValueError(f"Required keys not provided: {un_provided_keys}")

    def open_setup(self, step):
        # Create entity USD
        self.entity_usd = os.path.join(self.entity_path, f"{self.entity_name}.usda")
        UsdUtils.create_usd_file(self.entity_usd)

        # Create step USD
        step_usd = os.path.join(self.publish_dir, step, f"{self.entity_name}_{step}.usda")
        UsdUtils.create_usd_file(step_usd)
        self.step_usd_dict[step] = step_usd

    def process(self, step, provided_args):
        """ 클래스 이름을 문자열로 저장하고, getattr()을 사용해 동적으로 로드 """
        self.validate_args(step, provided_args)

        class_name = self.step_class_mapping.get(step)
        if not class_name:
            raise ValueError(f"Unsupported step: {step}")

        # getattr()을 사용하여 동적으로 클래스 가져오기
        step_class = getattr(self, class_name, None)
        if not step_class:
            raise ValueError(f"Step class {class_name} not found in {self.__class__.__name__}")

        # 동적으로 클래스 인스턴스 생성 및 실행
        processor = step_class(self)
        processor.process(**provided_args)

    # 내부 클래스들 정의
    class ModelUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, geo=None, **kwargs):
            print(f"Processing Model step with geo: {geo}")
            # Add reference
            pass

    class RigUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, **kwargs):
            print("Processing Rig step")
            pass

    class MatchmoveUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, camera=None, terrain=None, **kwargs):
            print(f"Processing Matchmove step with camera: {camera}, terrain: {terrain}")
            # Add camera sublayer
            pass

    class LayoutUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, assets_path=None, camera=None, **kwargs):
            if not camera:
                print("No camera path provided, adding camera over sublayer")
            print(f"Processing Layout step with assets_path: {assets_path}, camera: {camera}")
            # Add assets sublayer
            pass

    class AnimatingUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, cache=None, camera=None, **kwargs):
            if not camera:
                print("No camera path provided, adding camera over sublayer")
            print(f"Processing Animating step with cache: {cache}, camera: {camera}")
            # Add anim cache sublayer
            pass

    class LightingUsdProcessor:
        def __init__(self, parent):
            self.parent = parent

        def process(self, light=None, **kwargs):
            print(f"Processing Lighting step with light: {light}")
            # Add sublayer
            pass


if __name__ == "__main__":
    root_path = "/nas/sam/show/applestore/assets/Character/Bille/RIG/work/maya/scene.v012.ma"
    root1_path = "/nas/sam/show/applestore/assets/Character/Bille"

    processor = PublishUsdProcessor(root1_path)
    processor.process(MODELING, {"geo": "/path/to/geo.usda"})
    processor.process(MATCHMOVE, {"camera": "/path/to/camera.usda", "terrain": "/path/to/terrain.usda"})
