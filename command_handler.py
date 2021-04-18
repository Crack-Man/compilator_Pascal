import os.path
from lexer.lexer import Lexer

class CommandHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommandHandler, cls).__new__(cls)
        return cls.instance

    def execute_command(self, command):
        command_split = command.split(" ")
        command_lower = command_split[0].lower()
        if command_lower == "compiler":
            if len(command_split) == 4:
                type_analysis = command_split[1]
                object_analysis = command_split[2]
                path = command_split[3]
                if type_analysis == "-l":
                    if object_analysis == "-f":
                        if os.path.isfile(path):
                            try:
                                lexer = Lexer(path)
                                while lexer.notEOF():
                                    lex = lexer.findLexem()
                                    print(lex.getParams())
                            except UnicodeDecodeError as e:
                                print("'utf-8' codec can't decode byte")
                    elif object_analysis == "-d":
                        if os.path.isdir(path):
                            count_all = 0
                            count_failed = 0
                            for file in os.listdir(path):
                                try:
                                    if file.find("(result)") == -1:
                                        count_all += 1
                                        abs_path = os.path.join(path, file)
                                        split_file = os.path.splitext(abs_path)
                                        lexer = Lexer(abs_path)
                                        file_res = open(
                                            "{} (result){}".format(split_file[0], split_file[1]), "r", encoding="utf-8"
                                        )
                                        passed = True
                                        while lexer.notEOF():
                                            lex = lexer.findLexem()
                                            line = file_res.readline().replace("\n", "")
                                            if lex.getParams() != line:
                                                passed = False
                                                # print(lex.getParams())
                                        if not passed:
                                            count_failed += 1
                                        file_res.close()
                                        print("{} - {}".format(file, "OK" if passed else "WRONG"))
                                except UnicodeDecodeError as e:
                                    print("'utf-8' codec can't decode byte")
                            print("\nВсего тестов: {}\nИз них успешных: {}".format(count_all, count_all - count_failed))