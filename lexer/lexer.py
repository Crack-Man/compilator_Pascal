import string
from lexer.queue_token import QueueToken
from transitions import Machine

class Matter(object):
    pass

class Lexer:
    def __init__(self, path):
        self.path = path
        self.abc = [i for i in string.ascii_lowercase]
        self.numbers = [i for i in range(10)]
        self.ar_oper = ["+", "-", "*", "/", "div", "mod"]
        self.abs_coord = 1
        self.code = ""
        self.queue = QueueToken()

        with open(self.path, encoding="utf-8") as file_handler:
            for line in file_handler:
                self.code += line

        self.lump = Matter()
        self.states = ['Space', 'Comment', 'Identifier',
                       'Directive', 'Literal integer', 'Literal real',
                       'Literal string', 'Operation', 'Separator']

    def analysis(self):
        pass