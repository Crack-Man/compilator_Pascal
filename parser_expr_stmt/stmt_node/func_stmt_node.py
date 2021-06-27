from parser_expr_stmt.stmt_node.stmt_node import StmtNode
from parser_expr_stmt.stmt_node.null_stmt_node import NullStmtNode

class FuncStmtNode(StmtNode):
    def __init__(self, type_func, name, params, return_type, var, body):
        self.type_func = type_func
        self.name = name
        self.params = params
        self.return_type = return_type
        self.var = var
        self.body = body
        self.return_type = return_type

    def print(self, priority=1):
        tab = super().getTab()
        return_type = "void" if isinstance(self.return_type, NullStmtNode) else self.return_type.getValue()
        params = f"params\n{tab*(priority+1)}NONE" if isinstance(self.params, NullStmtNode) else self.params.print(priority+1)
        var = f"var\n{tab*(priority+1)}NONE" if isinstance(self.var, NullStmtNode) else self.var.print(priority+1)
        body = self.body.print(priority+1)
        return f"{self.type_func.getValue()} {self.name.getValue()}" \
               f"{f': {return_type}'}\n" \
               f"{tab*priority}{params}\n" \
               f"{tab*priority}{var}\n" \
               f"{tab*priority}{body}"

    def getValue(self):
        pass