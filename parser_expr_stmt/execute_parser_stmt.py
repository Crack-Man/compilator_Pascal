import os.path
from lexer.lexer import Lexer
from parser_expr_stmt.parser_stmt import ParserStmt
from compiler_exception import CompilerException

class ExecuteParserStmt:
    def __init__(self, range_of_analysis, path):
        self.range_of_analysis = range_of_analysis
        self.path = path
        self.compilerParser()

    def compilerParser(self):
        if self.range_of_analysis == 1:
            self.compilerParserFile()
        # elif self.range_of_analysis == 2:
        #     self.compilerParserDirectory()

    def compilerParserFile(self):
        if os.path.isfile(self.path):
            try:
                lexer = Lexer(self.path)
                lexer.getNextLexem()
                res = ParserStmt(lexer).parse()
                print(res.print())
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except CompilerException as e:
                print(e)
        else:
            print("ERROR")