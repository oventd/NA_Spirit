from abc import ABC, abstractmethod

class StepOpenMaya(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def open(self):
        pass
    
