from abc import ABC, abstractmethod

class StepOpenMaya(metaclass=ABC):
    #@abstractmethod
    #def validate(self)
    #    pass

    def __init__(self):
        pass
    @abstractmethod
    def open(self):
        pass
    
