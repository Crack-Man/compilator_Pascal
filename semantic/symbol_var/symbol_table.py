from semantic.symbol import Symbol

class SymTable(Symbol):
    def __init__(self):
        self.line = dict()

    def name(self):
        pass

    def newVarValue(self, var, value):
        self.line[var] = value