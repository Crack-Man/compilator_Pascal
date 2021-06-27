from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class ReadStmtNode(StmtNode):
    def __init__(self, type_read, identifier):
        self.type_read = type_read
        self.identifier = identifier

    def print(self, priority=1):
        tab = super().getTab()
        return f"{self.type_read.getValue()}\n{tab*priority}{self.identifier.getValue()}"

    def getValue(self):
        pass