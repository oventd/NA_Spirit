from abc import ABC, abstractmethod

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
        def __init__(self):
            pass

        @abstractmethod
        def validate(self):
            pass
        

