import os.path
from lexer.lexer import Lexer

class CommandHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommandHandler, cls).__new__(cls)
        return cls.instance

    def executeCommand(self, command):
        self.command_split = command.split(" ")
        command_lower = self.command_split[0].lower()
        if command_lower == "compiler":
            self.compiler()

    def compiler(self):
        if len(self.command_split) == 4:
            type_working = self.command_split[1]
            if type_working == "-l":
                self.compilerLexer()

    def compilerLexer(self):
        object_analysis = self.command_split[2]
        path = self.command_split[3]
        if object_analysis == "-f":
            self.compilerLexerFile(path)
        elif object_analysis == "-d":
            self.compilerLexerDirectory(path)


    def compilerLexerFile(self, path):
        if os.path.isfile(path):
            try:
                lexer = Lexer(path)
                lex = lexer.getLexem()
                print(lex.getParams())
                while lex.notEOF():
                    lex = lexer.getLexem()
                    print(lex.getParams())
            except UnicodeDecodeError:
                print(f"{path} 'utf-8' codec can't decode byte")
            except RuntimeError as e:
                print(e)
                print(lexer.getErrorLexem())

    def compilerLexerDirectory(self, path):
        if os.path.isdir(path):
            self.count_all = 0
            self.count_failed = 0
            self.error_file = os.path.join(path, 'log.txt')
            self.error_list = ""
            for file in os.listdir(path):
                try:
                    abs_path = os.path.join(path, file)
                    self.testFile(file, abs_path)
                except UnicodeDecodeError:
                    print(f"{abs_path} 'utf-8' codec can't decode byte")
            print(f"\nВсего тестов: {self.count_all}\nИз них успешных: {self.count_all - self.count_failed}")

    def testFile(self, file, path):
        if file.find("(result)") == -1 and file != "log.txt":
            self.count_all += 1
            split_file = os.path.splitext(path)
            lexer = Lexer(path)
            file_res = open(f"{split_file[0]} (result){split_file[1]}", "r", encoding="utf-8")
            self.passed = True
            try:
                lex = lexer.getLexem()
                self.compareResult(lex, file_res)
                while lex.notEOF():
                    lex = lexer.getLexem()
                    self.compareResult(lex, file_res)
            except RuntimeError as e:
                self.error_list += str(e)
                lex = lexer.getErrorLexem()
                self.compareResult(lex, file_res)
            finally:
                if not self.passed:
                    self.count_failed += 1
                file_res.close()
                print("{} - {}".format(file, "OK" if self.passed else "WRONG"))
                with open(self.error_file, "w") as error_file:
                    error_file.write(self.error_list)

    def compareResult(self, lexem, file):
        correct = file.readline().replace("\n", "")
        lex = lexem.getParams()
        if lex != correct:
            self.passed = False
            print(lex)