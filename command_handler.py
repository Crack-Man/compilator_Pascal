from lexer.execute_lexer import ExecuteLexer
from parser_expr.execute_parser import ExecuteParser

class CommandHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommandHandler, cls).__new__(cls)
        return cls.instance

    def executeCommand(self, command):
        self.command = command
        command_lower = self.command[1].lower()
        if command_lower == "compiler":
            self.compiler()

    def compiler(self):
        if len(self.command) == 5:
            type_working = self.command[2]
            if type_working == "-l":
                ExecuteLexer(self.command)
            elif type_working == "-p":
                ExecuteParser(self.command)