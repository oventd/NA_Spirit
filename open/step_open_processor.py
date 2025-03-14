import os
import sys
import shutil
import re

import logging

current_file_path = os.path.abspath(__file__)
spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../../"))
utils_dir = os.path.abspath(os.path.join(spirit_dir, "utils"))
sys.path.append(utils_dir)

from class_loader import load_classes_from_json
from sg_path_utils import SgPathUtils

# 로깅 설정 (필요에 따라 파일 로깅 등 추가 가능)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class OpenManager:
    def __init__(self, step:str) -> None:
        self.step = step
        dcc_config_path = "/home/rapa/NA_Spirit/open/config/open_step.json"
        self.types = ["assets", "sequences"]
        self.default_file = "scene"
        
        self.dcc_opens = load_classes_from_json(dcc_config_path)
        self.validate_inputs()

        self.open_class = self.dcc_opens[self.step]

    def validate_inputs(self) -> None:
        """
        entity_type과 dcc가 올바른지 검증합니다.
        """
        if self.step not in self.dcc_opens:
            raise ValueError(f"Invalid step: {self.step}. Please choose one of: {', '.join(self.dcc_opens.keys())}.")
        
    def open_setup(self) -> None:
        self.open_class.Open.setup()
    
    def validate(self):
        self.open_class.Publish.validate()
    
    def open(self):
        self.open_class.Publish.publish(sess, )
        
        
        
        






if __name__ == "__main__":
