from abc import ABC, abstractmethod
from parser_expr_stmt.node import Node

class ExprNode(Node, ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def getValue(self):
        pass