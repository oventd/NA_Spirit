import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))+'/utils'
sys.path.append(utils_dir)

from constant import *

from sg_path_utils import SgPathUtils

class PublishUsdProcessor:

    def __init__(self, entity_path:str):

        self.entity_path = self.trim_entity_path(entity_path)
        self.entity_name = os.path.basename(entity_path)

        self.entity_type = SgPathUtils.get_entity_type(entity_path)
        
        self.entity_usd = os.path.join(self.entity_path, f"{self.entity_name}.usd")
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

    

if __name__ == "__main__":
    root_path = "/nas/sam/show/applestore/assets/Character/Bille/RIG/work/maya/scene.v012.ma"
    root1_path = "/nas/sam/show/applestore/assets/Character/Bille"
    print(    SgPathUtils.trim_entity_path(root1_path))
    # usd = UsdProcessor(root_path)
    # usd.process(MODELING, geo = "", camera= "")