from parser_expr.node import Node

class BinOpNode(Node):
    def __init__(self, operation, left_operand, right_operand):
        self.operation = operation
        self.left_operand = left_operand
        self.right_operand = right_operand

    def print(self, priority=1):
        left_operand = self.left_operand.getValue()
        right_operand = self.right_operand.getValue()
        operation = self.operation.getValue()
        tab = "        "
        if isinstance(self.right_operand, BinOpNode):
            right_operand = self.right_operand.print(priority=priority+1)
        if isinstance(self.left_operand, BinOpNode):
            left_operand = self.left_operand.print(priority=priority+1)
        return f"{operation}\n{tab*priority}{left_operand}\n{tab*priority}{right_operand}"

    def getValue(self):
        pass