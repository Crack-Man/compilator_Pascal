from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class WriteStmtNode(StmtNode):
    def __init__(self, type_read, value):
        self.type_read = type_read
        self.value = value

    def print(self, priority=1):
        tab = super().getTab()
        value = self.value.print(priority+1)
        return f"{self.type_read.getValue()}\n{tab*priority}{value}"

    def getValue(self):
        pass