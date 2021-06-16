from parser_expr.node import Node

class UnOpNode(Node):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

    def print(self, priority=1):
        return f"{self.operation.getValue()}{self.operand.getValue()}"

    def getValue(self):
        pass