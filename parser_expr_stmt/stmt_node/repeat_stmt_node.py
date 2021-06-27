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
        if nodes[len(nodes)-1:] == "\n":
            nodes = nodes[:len(nodes)-1]
        return f"repeat\n{tab*priority}{nodes}\n" \
               f"until\n{tab*priority}{cond}" \

    def getValue(self):
        pass