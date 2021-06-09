from parser_expr.node import Node

class IdntNode(Node):
    def __init__(self, token):
        self.token = token

    def getValue(self):
        return self.token.getValue()

    def print(self):
        pass