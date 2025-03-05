import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))+'/utils'
sys.path.append(utils_dir)

from constant import *

class UsdProcessor:

    def __init__(self):
        self.step_publish_data_dict = {
            MODELING : ['geo'],
            # LOOKDEV : [],
            RIGGING : [],
            MATCHMOVE : ["camera", "terrain"],
            LAYOUT : ["camera", "terrain"],
            ANIMATION : ["camera", "terrain", "anim_cache"],
            LIGHTING : ["light"],
             
        }

    @staticmethod
    def get_arg_dict(geo= None, char = None, anim_cache = None, terrain = None, camera = None, light = None):
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
        elif step == ANIMATION:
            print("UsdProcessor Animate")
        elif step == LIGHTING:
            print("UsdProcessor Lighting")

    
    
    

if __name__ == "__main__":
    usd = UsdProcessor()
    usd.process(MODELING, geo = "", camera= "")