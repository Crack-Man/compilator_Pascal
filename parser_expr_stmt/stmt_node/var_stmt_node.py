from parser_expr_stmt.stmt_node.stmt_node import StmtNode
from parser_expr_stmt.node import Node

class VarStmtNode(StmtNode):
    def __init__(self, var, type_var):
        self.var = var
        self.type_var = type_var

    def print(self, priority=1):
        tab = super().getTab()
        var = f"{self.type_var}\n"
        for identifier in self.var.keys():
            data_type = self.var.get(identifier)
            var += f"{tab*priority}{identifier.getValue()} : {data_type.getValue()}\n"
        if var[len(var)-1:] == "\n":
            var = var[:len(var)-1]
        return var

    def getValue(self):
        pass