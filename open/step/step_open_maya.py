from abc import ABC, abstractmethod

class StepOpenMaya(ABC):
    #@abstractmethod
    #def validate(self)
    #    pass

    def __init__(self):
        pass

    """ 추상 클래스로 각 스텝에서 사용할 메서드를 정의함"""
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def validate(self):
        pass
    
