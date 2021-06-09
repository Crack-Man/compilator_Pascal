from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def getValue(self):
        pass