import os.path
from lexer.lexer import Lexer
from parser_expr_stmt.parser_expr import ParserExpr
from compiler_exception import CompilerException

class ExecuteParser:
    def __init__(self, range_of_analysis, path):
        self.range_of_analysis = range_of_analysis
        self.path = path
        self.compilerParser()

    def compilerParser(self):
        if self.range_of_analysis == 1:
            self.compilerParserFile()
        elif self.range_of_analysis == 2:
            self.compilerParserDirectory()

    def compilerParserFile(self):
        if os.path.isfile(self.path):
            try:
                lexer = Lexer(self.path)
                lexer.getNextLexem()
                res = ParserExpr(lexer).parseExpr()
                if res:
                    res = res.print()
                print(res)
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except CompilerException as e:
                print(e)
        else:
            print("ERROR")

    def compilerParserDirectory(self):
        if os.path.isdir(self.path):
            self.count_all = 0
            self.count_failed = 0
            self.error_file = os.path.join(self.path, 'log.txt')
            self.error_list = ""
            for file in os.listdir(self.path):
                try:
                    abs_path = os.path.join(self.path, file)
                    self.testFileParser(file, abs_path)
                except UnicodeDecodeError:
                    print(f"{abs_path} 'utf-8' codec can't decode byte")
            print(f"\nВсего тестов: {self.count_all}\nИз них успешных: {self.count_all - self.count_failed}")

    def testFileParser(self, file, path):
        if file[len(file) - 10:] == "(code).txt":
            self.count_all += 1
            split_file = os.path.splitext(path)
            file_res = open(split_file[0][:len(split_file[0]) - 7] + split_file[1], "r", encoding="utf-8")
            self.passed = True
            try:
                lexer = Lexer(path)
                lexer.getNextLexem()
                res = ParserExpr(lexer).parseExpr()
                if res:
                    res = res.print()
                self.compareResultParser(res, file_res)
            except CompilerException as e:
                self.compareResultParser(str(e), file_res)
            finally:
                if not self.passed:
                    self.count_failed += 1
                file_res.close()
                print("{} - {}".format(file, "OK" if self.passed else "WRONG"))

    def compareResultParser(self, res, file):
        correct = file.read()
        if res != correct:
            self.passed = False