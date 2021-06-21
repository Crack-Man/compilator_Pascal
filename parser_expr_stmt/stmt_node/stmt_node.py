from parser_expr_stmt.node import Node
from abc import ABC, abstractmethod

class StmtNode(Node, ABC):
    def getTab(self):
        return "        "

    @abstractmethod
    def print(self, priority=1):
        pass

    @abstractmethod
    def getValue(self):
        pass