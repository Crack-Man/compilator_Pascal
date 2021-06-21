from abc import ABC, abstractmethod

class Symbol(ABC):
    @abstractmethod
    def name(self):
        pass