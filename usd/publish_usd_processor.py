import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))+'/utils'
sys.path.append(utils_dir)

from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils

class PublishUsdProcessor:

    def __init__(self, entity_path:str):

        self.entity_path = SgPathUtils.trim_entity_path(entity_path)
        self.entity_name = os.path.basename(entity_path)
        self.entity_usd_path=""

        self.entity_type = SgPathUtils.get_entity_type(entity_path)
        
        self.publish_dir = os.path.join(self.entity_path, "publish")

        self.step_publish_data_dict = {
            MODELING : ['geo'],
            # LOOKDEV : [],
            RIGGING : [],
            MATCHMOVE : ["camera", "terrain"],
            LAYOUT : ["camera", "terrain"],
            ANIMATING : ["camera", "terrain", "anim_cache"],
            LIGHTING : ["light"],
        }
        self.step_usd_dict = {}
        
    
    @staticmethod
    def get_arg_dict(
        geo= None, 
        char = None, 
        anim_cache = None, 
        terrain = None, 
        camera = None, 
        light = None
        ):
        
        provided_args = {
            "geo": geo,
            "char": char,
            "anim_cache": anim_cache,
            "terrain": terrain,
            "camera": camera,
            "light": light
        }
        return provided_args

    def validate_args(self, step, provided_args):
        if self.step_publish_data_dict.get(step) is None:
            raise ValueError(f"Invalid step: {step}")

        required_keys = self.step_publish_data_dict.get(step, [])

        un_provied_keys = []
        for arg in provided_args.keys():
            if arg in required_keys and provided_args[arg] is None:
                un_provied_keys.append(arg)

        if len(un_provied_keys) > 0:
            raise ValueError(f"Required keys not provided: {un_provied_keys}")
    
    def open_setup(self, step):
        # entity usd를 만듬
        self.entity_usd = os.path.join(self.entity_path, f"{self.entity_name}.usda")
        UsdUtils.create_usd_file(self.entity_usd)

        # step usd를 만듬
        step_usd = os.path.join(self.publish_dir, step, f"{self.entity_name}_{step}.usda")
        UsdUtils.create_usd_file(step_usd)
        self.step_usd_dict[step] = step_usd

    def process(self, step, provided_args):
        self.validate_args(step, provided_args)

        if step == MODELING:
            print("UsdProcessor Model")
        elif step == RIGGING:
            print("UsdProcessor Rig")
        elif step == MATCHMOVE:
            print("UsdProcessor MatchMove")
        elif step == LAYOUT:
            print("UsdProcessor Layout")
        elif step == ANIMATING:
            print("UsdProcessor Animate")
        elif step == LIGHTING:
            print("UsdProcessor Lighting")
            
	class Model:
		def process(geo_path):
			#add reference
			pass
	class Rig:
		def process():
			pass
	class Matchmove:
		def process(camera_path):
			#add camera sublayer
			pass
	class Layout:
		def process(assets_path, camera_path=None):
			if not camera_path:
				#add camera over sublayer
			#add assets sublayer
			#add 
			pass
	class Animating(cache_path, camera_path=None):
		def process():
			if not camera_path:
				#add camera over sublayer
			#add anim cache sublayer
			pass
	class Lighting:
		def process(light_path):
			#add sublayer
			pass
		
	

if __name__ == "__main__":
    root_path = "/nas/sam/show/applestore/assets/Character/Bille/RIG/work/maya/scene.v012.ma"
    root1_path = "/nas/sam/show/applestore/assets/Character/Bille"
    print( SgPathUtils.trim_entity_path(root1_path))
    # usd = UsdProcessor(root_path)
    # usd.process(MODELING, geo = "", camera= "")