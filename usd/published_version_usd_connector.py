import os
import sys
utils_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../"))+'/utils'
sys.path.append(utils_dir)

from constant import *
from usd_utils import UsdUtils
from sg_path_utils import SgPathUtils

class PublishUsd2StepUsdConnector:

    @staticmethod
    def get_root_path(published_version):
        dir_path = os.path.dirname(published_version)
        base_name = os.path.basename(published_version)
        
        name, ext = os.path.splitext(base_name)
        file_name, version = name.split(".") # 파일명과 버전 분리

        result = os.path.join(dir_path, file_name+ext)
        return result
    
    
    @staticmethod
    def connect(publish_file_path):
        root_path = PublishUsd2StepUsdConnector.get_root_path(published_version)
        version = SgPathUtils.get_version(published_version)

        if not os.path.exists(root_path):
            UsdUtils.create_usd_file(root_path)

        stage = UsdUtils.get_stage(root_path)
        if not stage:
            stage = UsdUtils.create_stage(root_path)
        
        root_prim_path = "/Root"
        root_scope = UsdUtils.get_prim(stage, root_path)
        if not root_scope:
            root_scope = UsdUtils.create_scope(stage, root_prim_path)

        UsdUtils.add_refernce_to_variant_set(root_scope,"version", {version: publish_file_path}, set_default = True)

        return root_path

    
if __name__ == "__main__":
    published_version = "/nas/spirit/spirit/assets/Prop/apple/MDL/publish/maya/scene.v001.usd"

    root_path = PublishUsd2StepUsdConnector.get_root_path(published_version)
    print(root_path)

    print(PublishUsd2StepUsdConnector.connect(published_version))
