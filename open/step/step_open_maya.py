from abc import ABC, abstractmethod
import os
import sys
sys.path.append('/home/rapa/NA_Spirit/utils')
from json_utils import JsonUtils

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
        
        

