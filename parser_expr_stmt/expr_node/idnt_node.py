from parser_expr_stmt.expr_node.expr_node import ExprNode
from lexer.token import Token

class IdntNode(ExprNode):
    def __init__(self, token):
        self.token = token

    def getValue(self):
        return self.token.getValue() if isinstance(self.token, Token) else self.token.print()

    def print(self, priority=1):
        return str(self.token.getValue() if isinstance(self.token, Token) else self.token.print(priority))