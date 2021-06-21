from parser_expr_stmt.expr_node.expr_node import ExprNode

class CallNode(ExprNode):
    def __init__(self, name, params):
        self.name = name
        self.params = params

    def print(self):
        pass

    def getValue(self):
        pass