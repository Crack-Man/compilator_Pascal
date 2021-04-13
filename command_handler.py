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
        if command_lower == "lexer":
            if len(command_split) > 1:
                if os.path.isfile(command_split[1]):
                    try:
                        lexer = Lexer(command_split[1])
                        lexer.analysis()
                        lexer.printLex()
                    except UnicodeDecodeError as e:
                        print("'utf-8' codec can't decode byte")
                else:
                    print("File not found.")
            else:
                print("Enter the path to the file.")
        elif command_lower == "lexers":
            if len(command_split) > 1:
                if os.path.isdir(command_split[1]):
                    for file in os.listdir(command_split[1]):
                        try:
                            if file.find("(result)") == -1:
                                print(file)
                                abs_path = os.path.join(command_split[1], file)
                                split_file = os.path.splitext(abs_path)
                                lexer = Lexer(abs_path)
                                lexer.analysis()
                                new_file = "{} (result).txt".format(split_file[0])
                                with open(os.path.join(command_split[1], new_file), "w+") as file:
                                    for lex in lexer.getLex():
                                        file.write(lex.getParams())
                        except UnicodeDecodeError as e:
                            print("'utf-8' codec can't decode byte")
                else:
                    print("Directory not found.")
            else:
                print("Enter the path to the directory.")
        else:
            print("Command not found.")