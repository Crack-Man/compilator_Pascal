from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class BlockStmtNode(StmtNode):
    def __init__(self, stmt_node):
        self.stmt_node = stmt_node

    def print(self, priority=1):
        priority -= 1
        tab = super().getTab()
        nodes = ""
        for index, node in enumerate(self.stmt_node):
            nodes += f"{tab*priority if index else ''}{node.print(priority=priority+1)}\n"
        if nodes[len(nodes)-1:] == "\n":
            nodes = nodes[:len(nodes)-1]
        return f"{nodes}"

    def getValue(self):
        pass