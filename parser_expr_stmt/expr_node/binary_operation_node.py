from parser_expr_stmt.expr_node.expr_node import ExprNode
from parser_expr_stmt.expr_node.unary_operation_node import UnOpNode

class BinOpNode(ExprNode):
    def __init__(self, operation, left_operand, right_operand):
        self.operation = operation
        self.left_operand = left_operand
        self.right_operand = right_operand

    def print(self, priority=1):
        operation = self.operation.getValue()
        tab = "        "
        right_operand = self.right_operand.print(priority=priority+1)
        left_operand = self.left_operand.print(priority=priority+1)
        return f"{operation}\n{tab*priority}{left_operand}\n{tab*priority}{right_operand}"

    def getValue(self):
        pass