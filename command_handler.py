from lexer.execute_lexer import ExecuteLexer
from parser_expr.execute_parser import ExecuteParser

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
                ExecuteLexer(self.command_split)
            elif type_working == "-p":
                ExecuteParser(self.command_split)