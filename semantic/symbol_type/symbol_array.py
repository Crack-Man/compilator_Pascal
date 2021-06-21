from semantic.symbol_type.symbol_type import SymType

class SymArray(SymType):
    def __init__(self, sym_type):
        self.sym_type = sym_type