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

        self.step_publish_data_dict = {
            MODELING: ["geo"],
            RIGGING: [],
            LOOKDEV: ["material"],
            MATCHMOVE: ["camera"],
            LAYOUT: ["Asset"],
            ANIMATING: ["anim_cache"],
            LIGHTING: ["light"],
        }
        self.step_usd_dict = {}

        # Step을 문자열로 선언하여 객체를 동적으로 불러올 수 있도록 변경
        self.step_class_mapping = {
            MODELING: "Model",
            RIGGING: "Rig",
            LOOKDEV: "Lookdev",
            MATCHMOVE: "Matchmove",
            LAYOUT: "Layout",
            ANIMATING: "Animating",
            LIGHTING: "Light",
        }

    @staticmethod
    def get_arg_dict(geo=None, char=None, anim_cache=None, terrain=None, camera=None, light=None):
        return {
            "geo": geo,
            "Asset": char,
            "anim_cache": anim_cache,
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
        if os.path.exists(self.entity_usd_path):
            self.entity_usd_stage = UsdUtils.get_stage(self.entity_usd_path)
            
        if not os.path.exists(self.entity_usd_path):
            self.entity_usd_stage = UsdUtils.create_usd_file(self.entity_usd_path)

        root_path = "/Root"    
        try:
            self.entity_root_prim = self.entity_usd_stage.GetPrimAtPath(root_path)
        except:
            self.entity_root_prim = UsdUtils.create_scope(self.entity_usd_stage,root_path)
        
        step_usd = os.path.join(self.publish_dir, self.step, f"{self.entity_name}_{self.step}.usda")
        UsdUtils.create_usd_file(step_usd)

        self.step_usd_dict[self.step] = step_usd

    def process(self, step, provided_args):
        """ 클래스 이름을 문자열로 저장하고, getattr()을 사용해 동적으로 로드 """
        if step is RIGGING:
            return
        
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

        def process(self, geo_path):
            print(f"Processing Model step with geo: {geo_path}")
            if geo_path:
                geo_xform_path = os.path.join(self.parent.entity_root_prim.GetPath(),"geo")
                geo_xform =UsdUtils.create_xform(self.parent.entity_usd_stage, geo_xform_path)
                UsdUtils.add_reference(geo_xform, geo_path)


    class Lookdev:
        def __init__(self, parent):
            self.parent = parent
        def process(self, material_path):
            print(f"Processing Lookdev step with material: {material_path}")
            if material_path:
                material_xform_path = os.path.join(self.parent.entity_root_prim.GetPath(),"mat")
                mat_xform =UsdUtils.create_xform(self.parent.entity_usd_stage, material_xform_path)
                UsdUtils.add_reference(mat_xform, material_path)

    class Matchmove:
        def __init__(self, parent):
            self.parent = parent

        def process(self, camera_path):
            print(f"Processing Matchmove step with camera: {camera_path}")
            if camera_path:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, camera_path)


    class Layout:
        def __init__(self, parent):
            self.parent = parent

        def process(self, asset_path, camera_path=None):
            print(f"Processing Layout step with assets_path: {asset_path}, camera: {camera_path}")
            if camera_path:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, camera_path)
            if asset_path:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, asset_path)
            
    class Animating:
        def __init__(self, parent):
            self.parent = parent

        def process(self, anim_cache_path=None, camera_path=None):
            print(f"Processing Animating step with anim_cache: {anim_cache_path}, camera: {camera_path}")
            if camera_path:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, camera_path)
            if anim_cache_path:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, anim_cache_path)

    class Light:
        def __init__(self, parent):
            self.parent = parent

        def process(self, light=None):
            print(f"Processing Lighting step with light: {light}")
            if light:
                UsdUtils.add_sublayer(self.parent.entity_usd_stage, light)


if __name__ == "__main__":
    root1_path = "/nas/sam/show/applestore/assets/Character/Bille"

    processor = PublishUsdProcessor(root1_path)
    processor.process(MODELING, {"geo": "/path/to/geo.usda"})
    processor.process(MATCHMOVE, {"camera": "/path/to/camera.usda", "terrain": "/path/to/terrain.usda"})
