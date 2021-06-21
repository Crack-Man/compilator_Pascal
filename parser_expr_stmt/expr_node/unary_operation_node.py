from parser_expr_stmt.expr_node.expr_node import ExprNode

class UnOpNode(ExprNode):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

    def print(self, priority=None):
        return f"{self.operation.getValue()}{self.operand.getValue()}"

    def getValue(self):
        pass