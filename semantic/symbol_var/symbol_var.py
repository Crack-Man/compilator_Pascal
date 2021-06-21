from semantic.symbol import Symbol

class SymVar(Symbol):
    def __init__(self, sym_type):
        self.sym_type = sym_type

    def name(self):
        pass