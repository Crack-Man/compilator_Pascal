from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class WhileStmtNode(StmtNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def print(self, priority=1):
        tab = super().getTab()
        cond = self.cond.print(priority=priority+1)
        body = self.body.print(priority=priority+1)
        return f"while\n{tab*priority}{cond}\n" \
               f"do\n{tab*priority}{body}\n" \

    def getValue(self):
        pass