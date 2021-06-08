from node import Node

class BinOpNode(Node):
    def __init__(self, token, left_operand, right_operand):
        self.token = token
        self.left_operand = left_operand
        self.right_operand = right_operand

    def print(self):
        pass