from abc import *

class Loader(metaclass=ABCMeta):
    
    @abstractmethod
    def import_file(self):
        pass
    @abstractmethod
    def reference_file(self):
        pass
    @abstractmethod
    def stage_file(self):
        pass

