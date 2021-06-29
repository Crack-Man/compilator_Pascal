from parser_expr_stmt.stmt_node.stmt_node import StmtNode
from parser_expr_stmt.node import Node
from lexer.token import Token

class AssignStmtNode(StmtNode):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def print(self, priority=1):
        tab = super().getTab()
        identifier = self.identifier.getValue() if isinstance(self.identifier, Token) else self.identifier.print(priority=priority)
        value = self.value.print(priority=priority+1)
        return f"{identifier}\n{tab*(priority-1)}:=\n{tab*priority}{value}"

    def getValue(self):
        pass