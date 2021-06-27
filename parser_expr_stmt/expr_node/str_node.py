from parser_expr_stmt.expr_node.expr_node import ExprNode

class StrNode(ExprNode):
    def __init__(self, value):
        self.value = value

    def print(self, priority=None):
        return f"{self.value.getValue()}"

    def getValue(self):
        pass