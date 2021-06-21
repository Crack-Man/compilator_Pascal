from parser_expr_stmt.stmt_node.stmt_node import StmtNode
from parser_expr_stmt.expr_node.expr_node import ExprNode

class IfStmtNode(StmtNode):
    def __init__(self, cond, body, body_else):
        self.cond = cond
        self.body = body
        self.body_else = body_else

    def print(self, priority=1):
        tab = super().getTab()
        cond = self.cond.print(priority=priority+1)
        body = self.body.print(priority=priority+1)
        body_else = self.body_else.print(priority=priority+1)
        return f"if\n{tab*priority}{cond}\n" \
               f"then\n{tab*priority}{body}\n" \
               f"else\n{tab*priority}{body_else}"

    def getValue(self):
        pass