from abc import ABC, abstractmethod

class Token(ABC):
    @abstractmethod
    def set_coordinates(self):
        pass

    @abstractmethod
    def get_coordinates(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def set_source(self):
        pass

    @abstractmethod
    def get_source(self):
        pass

    @abstractmethod
    def set_value(self):
        pass

    @abstractmethod
    def get_value(self):
        pass