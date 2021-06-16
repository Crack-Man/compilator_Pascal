import os.path
from lexer.lexer import Lexer

class ExecuteLexer:
    def __init__(self, range_of_analysis, path):
        self.range_of_analysis = range_of_analysis
        self.path = path
        self.compilerLexer()

    def compilerLexer(self):
        if self.range_of_analysis == 1:
            self.compilerLexerFile()
        elif self.range_of_analysis == 2:
            self.compilerLexerDirectory()


    def compilerLexerFile(self):
        if os.path.isfile(self.path):
            try:
                lexer = Lexer(self.path)
                lex = lexer.getNextLexem()
                print(lex.getParams())
                while lex.notEOF():
                    lex = lexer.getNextLexem()
                    print(lex.getParams())
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except RuntimeError as e:
                print(e)

    def compilerLexerDirectory(self):
        if os.path.isdir(self.path):
            self.count_all = 0
            self.count_failed = 0
            self.error_file = os.path.join(self.path, 'log.txt')
            self.error_list = ""
            for file in os.listdir(self.path):
                try:
                    abs_path = os.path.join(self.path, file)
                    self.testFileLexer(file, abs_path)
                except UnicodeDecodeError:
                    print(f"{abs_path} 'utf-8' codec can't decode byte")
            print(f"\nВсего тестов: {self.count_all}\nИз них успешных: {self.count_all - self.count_failed}")

    def testFileLexer(self, file, path):
        if file[len(file) - 10:] == "(code).txt":
            self.count_all += 1
            split_file = os.path.splitext(path)
            lexer = Lexer(path)
            file_res = open(split_file[0][:len(split_file[0]) - 7] + split_file[1], "r", encoding="utf-8")
            self.passed = True
            try:
                lex = lexer.getNextLexem()
                self.compareResultLexer(lex.getParams(), file_res)
                while lex.notEOF():
                    lex = lexer.getNextLexem()
                    self.compareResultLexer(lex.getParams(), file_res)
            except RuntimeError as e:
                self.compareResultLexer(str(e), file_res)
            finally:
                if not self.passed:
                    self.count_failed += 1
                file_res.close()
                print("{} - {}".format(file, "OK" if self.passed else "WRONG"))

    def compareResultLexer(self, lexem, file):
        correct = file.readline().replace("\n", "")
        if lexem != correct:
            self.passed = False
            print(lexem)