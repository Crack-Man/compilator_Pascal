from parser_expr_stmt.expr_node.expr_node import ExprNode

class IntNode(ExprNode):
    def __init__(self, token):
        self.token = token

    def getValue(self):
        return self.token.getValue()

    def print(self, priority=None):
        return str(self.token.getValue())