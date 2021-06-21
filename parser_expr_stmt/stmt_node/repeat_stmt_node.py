from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class UntilStmtNode(StmtNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self, priority=1):
        tab = super().getTab()
        cond = self.cond.print(priority=priority+1)
        nodes = ""
        for index, node in enumerate(self.body):
            nodes += f"{tab * priority if index else ''}{node.print(priority=priority + 1)}\n"
        return f"repeat\n{tab*priority}{nodes}" \
               f"until\n{tab*priority}{cond}\n" \

    def getValue(self):
        pass