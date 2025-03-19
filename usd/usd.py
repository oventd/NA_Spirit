import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))+'/utils'
print(utils_dir)
sys.path.append(utils_dir)
from constant import *
class UsdProcessor:

    def __init__(self):
        pass
    def process(self, step, geo= None, char = None, anim_cache = None, terrain = None, carmera = None, light = None):
        if step == MODELING:
            print("UsdProcessor Model")
        
    
    

