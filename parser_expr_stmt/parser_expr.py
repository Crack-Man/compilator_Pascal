from lexer.token_list import TokenList
from parser_expr_stmt.expr_node.idnt_node import IdntNode
from parser_expr_stmt.expr_node.int_node import IntNode
from parser_expr_stmt.expr_node.real_node import RealNode
from parser_expr_stmt.expr_node.binary_operation_node import BinOpNode
from parser_expr_stmt.expr_node.unary_operation_node import UnOpNode
from compiler_exception import CompilerException

class ParserExpr:
    def __init__(self, lexer):
        self.lexer = lexer

    def parseExpr(self):
        token = self.lexer.getCurrentLexem()
        if not token.notEOF() or token.getValue() == ';':
            raise CompilerException("Expected expression")
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
        if token.getValue() == "+" or token.getValue() == "-":
            operand = self.parseFactor()
            return UnOpNode(token, operand)
        if token.getValue() == "(":
            left = self.parseExpr()
            token = self.lexer.getCurrentLexem()
            if token.getValue() != ")":
                raise CompilerException("')' was expected")
            self.lexer.getNextLexem()
            return left
        raise CompilerException(f'Unexpected "{token.getCode()}"')