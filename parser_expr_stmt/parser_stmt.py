from lexer.token_list import TokenList
from parser_expr_stmt.parser_expr import ParserExpr
from compiler_exception import CompilerException
from enum import Enum

from parser_expr_stmt.stmt_node.block_stmt_node import BlockStmtNode
from parser_expr_stmt.stmt_node.while_stmt_node import WhileStmtNode
from parser_expr_stmt.stmt_node.repeat_stmt_node import UntilStmtNode
from parser_expr_stmt.stmt_node.for_stmt_node import ForStmtNode
from parser_expr_stmt.stmt_node.if_stmt_node import IfStmtNode
from parser_expr_stmt.stmt_node.assign_stmt_node import AssignStmtNode
from parser_expr_stmt.stmt_node.null_stmt_node import NullStmtNode


class Statements(Enum):
    stmt_begin = "begin"
    stmt_end = "end"

    stmt_while = "while"
    stmt_do = "do"
    stmt_repeat = "repeat"
    stmt_until = "until"
    stmt_for = "for"
    stmt_to = "to"
    stmt_downto = "downto"

    stmt_if = "if"
    stmt_then = "then"
    stmt_else = "else"
    stmt_separator = ";"

    stmt_procedure = "procedure"
    stmt_function = "function"
    stmt_l_bracket = "("
    stmt_r_bracket = ")"
    stmt_sepcolon = ":"
    stmt_return = "return"




class ParserStmt:
    def __init__(self, lexer):
        self.lexer = lexer

    def requireValue(self, stmt):
        token = self.lexer.getCurrentLexem()
        if token.getValue() != stmt.value:
            raise CompilerException(f"'{stmt.value}' was expected")
        self.lexer.getNextLexem()

    def requireType(self, stmt):
        token = self.lexer.getCurrentLexem()
        if token.getType() != stmt.value:
            raise CompilerException(f"'{stmt.value}' was expected")
        self.lexer.getNextLexem()

    def optional(self, stmt):
        token = self.lexer.getCurrentLexem()
        if token.getValue() != stmt.value:
            return False
        self.lexer.getNextLexem()
        return True

    def parseBlock(self):
        self.requireValue(Statements.stmt_begin)
        body = []
        while self.lexer.getCurrentLexem().getValue() != Statements.stmt_end.value:
            body.append(self.parse())
        self.requireValue(Statements.stmt_end)
        self.requireValue(Statements.stmt_separator)
        return BlockStmtNode(body)

    def parseWhile(self):
        self.requireValue(Statements.stmt_while)
        cond = ParserExpr(self.lexer).parseExpr()
        self.requireValue(Statements.stmt_do)
        body = self.parse()
        return WhileStmtNode(cond, body)

    def parseRepeat(self):
        self.requireValue(Statements.stmt_repeat)
        body = []
        while self.lexer.getCurrentLexem().getValue() != Statements.stmt_until.value:
            body.append(self.parse())
        self.requireValue(Statements.stmt_until)
        cond = ParserExpr(self.lexer).parseExpr()
        return UntilStmtNode(cond, body)

    def parseFor(self):
        self.requireValue(Statements.stmt_for)
        start = self.parseAssign(separator=False)
        step = self.lexer.getCurrentLexem()
        try:
            self.requireValue(Statements.stmt_downto)
        except CompilerException:
            self.requireValue(Statements.stmt_to)
        end = ParserExpr(self.lexer).parseExpr()
        self.requireValue(Statements.stmt_do)
        body = self.parse()
        return ForStmtNode(start, end, step, body)

    def parseIf(self):
        self.requireValue(Statements.stmt_if)
        cond = ParserExpr(self.lexer).parseExpr()
        self.requireValue(Statements.stmt_then)
        body = self.parse()
        body_else = self.parse() if self.optional(Statements.stmt_else) else NullStmtNode()
        return IfStmtNode(cond, body, body_else)

    def parseAssign(self, separator=True):
        identifier = self.lexer.getCurrentLexem()
        self.requireType(TokenList.identifier)
        self.requireType(TokenList.assignment)
        value = ParserExpr(self.lexer).parseExpr()
        if separator:
            self.requireValue(Statements.stmt_separator)
        return AssignStmtNode(identifier, value)

    def parse(self):
        token = self.lexer.getCurrentLexem()
        if token.getValue() == Statements.stmt_begin.value:
            return self.parseBlock()
        if token.getValue() == Statements.stmt_while.value:
            return self.parseWhile()
        if token.getValue() == Statements.stmt_repeat.value:
            return self.parseRepeat()
        if token.getValue() == Statements.stmt_for.value:
            return self.parseFor()
        if token.getValue() == Statements.stmt_if.value:
            return self.parseIf()
        if token.getType() == TokenList.identifier.value:
            return self.parseAssign()
        return None