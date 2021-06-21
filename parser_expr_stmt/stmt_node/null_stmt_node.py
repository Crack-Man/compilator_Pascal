from parser_expr_stmt.stmt_node.stmt_node import StmtNode

class NullStmtNode(StmtNode):
    def print(self, priority=1):
        return "NONE"

    def getValue(self):
        pass

