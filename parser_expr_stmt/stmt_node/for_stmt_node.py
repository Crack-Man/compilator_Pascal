from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class ForStmtNode(StmtNode):
    def __init__(self, start, stop, step, body):
        self.start = start
        self.stop = stop
        self.step = step
        self.body = body

    def print(self, priority=1):
        tab = super().getTab()
        start = self.start.print(priority=priority+1)
        stop = self.stop.print(priority=priority + 1)
        step = self.step.getValue()
        body = self.body.print(priority=priority+1)
        return f"for\n{tab*priority}{start}\n" \
               f"{step}\n{tab*priority}{stop}\n" \
               f"do\n{tab*priority}{body}\n" \

    def getValue(self):
        pass