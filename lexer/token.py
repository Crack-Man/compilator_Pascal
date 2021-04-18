class Token:
    def __init__(self):
        self.coordinates = ""
        self.type = ""
        self.code = ""
        self.value = ""

    def setParams(self, coordinates, type, code, value):
        self.coordinates = coordinates
        self.type = type
        self.code = code
        self.value = value

    def getCoordinates(self):
        return self.coordinates

    def getParams(self):
        if self.coordinates:
            return '{}        {}        "{}"        {}'.format(self.coordinates, self.type, self.code, self.value)
        return ''