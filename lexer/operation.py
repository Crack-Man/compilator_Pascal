from lexer.token import Token

class Operation(Token):
    def __init__(self):
        self.__coordinate = 0
        self.__type = "Operation"
        self.__source = ""
        self.__value = ""

    def set_coordinates(self, coordinate):
        self.__coordinate = coordinate

    def get_coordinates(self):
        return self.__coordinate

    def get_type(self):
        return self.__type

    def set_source(self, source):
        self.__source = source

    def get_source(self):
        return self.__source

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value