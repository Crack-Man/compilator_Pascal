from parser_expr_stmt.expr_node.expr_node import ExprNode
from lexer.token import Token

class ArrIndexNode(ExprNode):
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def print(self, priority=1):
        index = self.index.getValue() if isinstance(self.index, Token) else self.index.print(priority)
        return f"{self.value.getValue()}[{index}]"

    def getValue(self):
        pass