class Token:
    def __init__(self, coordinates, type, code, value):
        self.coordinates = coordinates
        self.type = type
        self.code = code
        self.value = value

    def getCoordinates(self):
        return self.coordinates

    def notEOF(self):
        return self.type != "EOF"

    def getParams(self):
        if self.notEOF():
            return f'{self.coordinates}        {self.type}        "{self.code}"        {self.value}'
        return ''