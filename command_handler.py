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
                        Lexer(command_split[1])
                    except UnicodeDecodeError as e:
                        print("'utf-8' codec can't decode byte")
                else:
                    print("File not found.")
            else:
                print("Enter the path to the file.")
        else:
            print("Command not found.")