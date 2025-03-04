from abc import ABC, abstractmethod

class StepOpenMaya(ABC):
    def __init__(self):
        print ("초기화")

    @abstractmethod
    def open(self):
        pass
    
