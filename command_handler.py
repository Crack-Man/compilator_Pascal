from lexer.execute_lexer import ExecuteLexer
from parser_expr_stmt.execute_parser import ExecuteParser
from parser_expr_stmt.execute_parser_stmt import ExecuteParserStmt
import os.path

class CommandHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommandHandler, cls).__new__(cls)
        return cls.instance

    def checkCommand(self, commands):
        type_working = 0
        range_of_analysis = 0
        path = ""
        for command in commands:
            command = command.lower()
            if command == "-l":
                type_working = 1
            if command == "-p":
                type_working = 2
            if command == "-ps":
                type_working = 3
            if command == "-f":
                range_of_analysis = 1
            if command == "-d":
                range_of_analysis = 2
            if os.path.isfile(command) or os.path.isdir(command):
                path = command
        if type_working:
            if range_of_analysis:
                if path:
                    if type_working == 1:
                        ExecuteLexer(range_of_analysis, path)
                    elif type_working == 2:
                        ExecuteParser(range_of_analysis, path)
                    elif type_working == 3:
                        ExecuteParserStmt(range_of_analysis, path)
                else:
                    print("You have not entered the path")
            else:
                print("You have not entered the range of work (file '-f' or directory '-d')")
        else:
            print("You have not entered the type of work of the compiler (lexer '-l' or parser '-p'")