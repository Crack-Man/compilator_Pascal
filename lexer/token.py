class Token:
    def __init__(self, coordinates, type, code, value):
        self.coordinates = coordinates
        self.type = type
        self.code = code
        self.value = value

    def getParams(self):
        return "Координата - {},\n\tТип - {},\n\tКод - '{}',\n\tЗначение - '{}'\n\n".format(self.coordinates, self.type, self.code, self.value)