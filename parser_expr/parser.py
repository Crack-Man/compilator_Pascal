from lexer.token_list import TokenList
from parser_expr.idnt_node import IdntNode
from parser_expr.int_node import IntNode
from parser_expr.real_node import RealNode
from parser_expr.binary_operation_node import BinOpNode
from parser_expr.unary_operation_node import UnOpNode

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lexer.getNextLexem()

    def parseExpr(self):
        token = self.lexer.getCurrentLexem()
        if not token.notEOF() or token.getValue() == ';':
            raise RuntimeError("Expected expression")
        if token.getValue() == "+" or token.getValue() == "-":
            self.lexer.getNextLexem()
            operand = self.parseFactor()
            left = UnOpNode(token, operand)
        else:
            left = self.parseTerm()
        operation = self.lexer.getCurrentLexem()
        while operation.getValue() == "+" or operation.getValue() == "-":
            self.lexer.getNextLexem()
            right = self.parseTerm()
            left = BinOpNode(operation, left, right)
            operation = self.lexer.getCurrentLexem()
        return left

    def parseTerm(self):
        left = self.parseFactor()
        operation = self.lexer.getCurrentLexem()
        while operation.getValue() == "*" or operation.getValue() == "/":
            self.lexer.getNextLexem()
            right = self.parseFactor()
            left = BinOpNode(operation, left, right)
            operation = self.lexer.getCurrentLexem()
        return left

    def parseFactor(self):
        token = self.lexer.getCurrentLexem()
        self.lexer.getNextLexem()
        if token.getType() == TokenList.identifier.value:
            return IdntNode(token)
        if token.getType() == TokenList.integer.value:
            return IntNode(token)
        if token.getType() == TokenList.real.value:
            return RealNode(token)
        if token.getValue() == "(":
            left = self.parseExpr()
            token = self.lexer.getCurrentLexem()
            if token.getValue() != ")":
                raise RuntimeError("')' was expected")
            self.lexer.getNextLexem()
            return left
        raise RuntimeError(f'Unexpected "{token.getCode()}"')