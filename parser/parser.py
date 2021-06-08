from binary_operation_node import BinOpNode
from idnt_node import IdntNode()

class Parser:
    def __init__(self, lex):
        self.lex = lex

    def parseExpr(self):
        # left = parseTerm()
        # Token op = lex.get()
        # if op == "+" or op == "-"
            # right = parseExpr()
            # return BinOpNode(op, left, right)
        # else
            # return left
        pass

    def parseTerm(self):
        # left = parseFactor()
        # Token op = lex.get()
        # if op == "*" or op == "/"
            # lex.next() ??
            # right = parseTerm()
            # return BinOpNode(op, left, right)
        # else
            # return left
        pass

    def parseFactor(self):
        # t = lex.get()
        # if t.type == identifier
            # return IdntNode(t)
        # if t.type == number
            # return IntNode
        # if t.type == "("
            # lex.next()
            # l = parseExpr()
        # if t.type == 4to-to
            # return ERROR "Ожидался символ, но его нет"
        # lex.next()
        # return l
        # throw error "Неожиданный символ"
        pass