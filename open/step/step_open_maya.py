from abc import ABC, abstractmethod
import maya.cmds as cmds
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/utils')
from json_utils import JsonUtils
from maya_utils import MayaUtils

class StepOpenMaya(ABC):
    def __init__(self):
        pass
    
    # Open 클래스: 'setup' 관련 기능을 다룬다.    
    class Open(ABC):
        @abstractmethod
        def setup(self):
            pass

    # Publish 클래스: 퍼블리시 관련 기능을 다룬다.    
    class Publish(ABC):

        _publish_settings = None  # JSON 캐싱
        _render_settings = None  # JSON 캐싱

        def __init__(self):
            pass

        @classmethod
        def get_publish_settings(cls):
            if cls._publish_settings is None:
                cls._publish_settings = JsonUtils.read_json("/home/rapa/NA_Spirit/open/config/publish_settings.json")
            return cls._publish_settings  

        @classmethod     
        def get_render_settings(cls):
            if cls._render_settings is None:
                cls._render_settings = JsonUtils.read_json("/home/rapa/NA_Spirit/open/config/render_settings.json")
            return cls._render_settings
        
        @abstractmethod
        def validate(self):
            pass
        
        @abstractmethod
        def publish(self):
            pass

        @staticmethod
        def export_setting(group_name, step, file_path=""):
            """ 퍼블리싱을 위한 공통 export 설정 로직 """
            publish_settings = StepOpenMaya.Publish.get_publish_settings()

            # Step이 존재하는지 확인
            step_settings = publish_settings.get(step)
            if step_settings is None:
                print(f"Error: Step '{step}' not found in publish settings.")
                return {}

            # group_name (예: "geo")에 해당하는 설정이 있는지 확인
            group_settings = step_settings.get(group_name)
            if not group_settings:
                print(f"Warning: No settings found for group '{group_name}' in step '{step}'.")
                return {}

            for key, value in group_settings.items():
                if value.get("all", False):
                    children = cmds.listRelatives(group_name, children=True) or []
                    print(f"Importing all children of {group_name} at once.")
                else:
                    children = cmds.listRelatives(group_name, children=False) or []
                    print(f"Importing specific children of {group_name}.")
            
            if value.get("isReferenced", False):
                if not file_path:
                    print("Error: file_path is required for referenced objects.")
                    return {}
                else:
                    MayaUtils.reference_file(file_path, group_name)

            return group_settings
            
        @staticmethod
        def render_setting(step, category, group):
            """ 렌더링 설정을 가져오는 메서드 """
            render_settings = StepOpenMaya.Publish.get_render_settings()

            # Step이 존재하는지 확인
            step_settings = render_settings.get(step, {})
            if not step_settings:
                print(f"Warning: No render settings found for step '{step}'. Using defaults.")
                return {}

            return step_settings.get(category, {}).get(group, {})
   

        
        

