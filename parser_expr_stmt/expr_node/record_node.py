from parser_expr_stmt.expr_node.expr_node import ExprNode

class RecordNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def print(self):
        pass

    def getValue(self):
        pass