from parser_expr.node import Node

class IntNode(Node):
    def __init__(self, token):
        self.token = token

    def getValue(self):
        return self.token.getValue()

    def print(self):
        return str(self.token.getValue())