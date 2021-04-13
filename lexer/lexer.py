from lexer.queue_token import QueueToken
from lexer.token import Token

class Lexer:
    def __init__(self, path):
        self.path = path
        self.reserved = {"and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "div", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "mod", "nil", "not", "object",
                         "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}
        self.predefined = {"abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eof", "eoln", "exp",
                           "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                           "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                           "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}
        self.space_symbols = {' ', '\n', '\t', '\0', '\r'}
        self.admissible = {',', ':', ';', '(', ')', '[', ']', '+', '-', '*', '/'}
        self.operations = {'+', '-', '*', '/'}
        self.separators = {',', ';'}
        self.code = ""

        with open(self.path, encoding="utf-8") as file:
            for line in file:
                self.code += line

        self.state = "Space"
        self.buf = ""
        self.lexes = QueueToken()
        self.index = 0

    def analysis(self):
        coordinate = 0
        while self.state != "Final":
            if self.state == "Space":
                if self.code[self.index] in self.space_symbols:
                    coordinate = self.index + 1
                    self.lexes.pushLex(Token(coordinate, "Space", self.code[self.index].encode("unicode_escape").decode("utf-8"), self.code[self.index].encode("unicode_escape").decode("utf-8")))
                    self.getNext()
                elif self.code[self.index].isalpha():
                    coordinate = self.index + 1
                    self.state = "Identifier"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index].isdigit():
                    coordinate = self.index + 1
                    self.state = "Integer"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] in self.operations:
                    coordinate = self.index + 1
                    self.state = "Operation"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == '{':
                    coordinate = self.index + 1
                    self.state = "Comment"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == ':':
                    coordinate = self.index + 1
                    self.state = "Assignment"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == '.':
                    self.state = "Final"
                    coordinate = self.index + 1
                    self.lexes.pushLex(Token(coordinate, "Separator", self.code[self.index], self.code[self.index]))
                elif self.code[self.index] in self.separators:
                    self.state = "Separator"
                    self.lexes.pushLex(Token(coordinate, "Separator", self.code[self.index], self.code[self.index]))
                    coordinate = self.index + 1
                    self.getNext()
                else:
                    self.state = "Error"
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Identifier":
                if self.code[self.index].isdigit() or self.code[self.index].isalpha():
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == '.':
                    self.state = "Final"
                    if self.buf.lower() in self.reserved:
                        self.lexes.pushLex(Token(coordinate, "Reserved Word", self.buf, self.buf))
                    elif self.buf.lower() in self.predefined:
                        self.lexes.pushLex(Token(coordinate, "Predefined Word", self.buf, self.buf))
                    else:
                        self.lexes.pushLex(Token(coordinate, "Identifier", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                    self.lexes.pushLex(Token(coordinate, "Separator", self.code[self.index], self.code[self.index]))
                elif self.code[self.index] in self.admissible or self.code[self.index] in self.space_symbols:
                    self.state = "Space"
                    if self.buf.lower() in self.reserved:
                        self.lexes.pushLex(Token(coordinate, "Reserved Word", self.buf, self.buf))
                    elif self.buf.lower() in self.predefined:
                        self.lexes.pushLex(Token(coordinate, "Predefined Word", self.buf, self.buf))
                    else:
                        self.lexes.pushLex(Token(coordinate, "Identifier", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                else:
                    self.state = "Error"
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Integer":
                if self.code[self.index].isdigit():
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == ".":
                    self.state = "Real"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] in self.admissible or self.code[self.index] in self.space_symbols:
                    self.state = "Space"
                    self.lexes.pushLex(Token(coordinate, "Integer", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                else:
                    self.state = "Error"
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Real":
                if self.code[self.index].isdigit():
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] in self.admissible or self.code[self.index] in self.space_symbols:
                    self.state = "Space"
                    self.lexes.pushLex(Token(coordinate, "Real", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                else:
                    self.state = "Error"
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Operation":
                if self.code[self.index] == '*':
                    self.state = "Space"
                    self.addBuf(self.code[self.index])
                    self.lexes.pushLex(Token(coordinate, "Operation", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                    self.getNext()
                elif self.code[self.index] == '=':
                    self.state = "Space"
                    self.addBuf(self.code[self.index])
                    self.lexes.pushLex(Token(coordinate, "Assignment", self.buf, self.buf))
                    self.clearBuf()
                    coordinate = self.index + 1
                    self.getNext()
                elif self.code[self.index] == ' ' or self.code[self.index].isalpha() or self.code[self.index].isdigit():
                    self.state = "Space"
                    self.lexes.pushLex(Token(coordinate, "Operation", self.buf, self.buf))
                    self.clearBuf()
                else:
                    self.state = "Error"
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Comment":
                if self.code[self.index] == "$" and len(self.buf) == 1:
                    self.state = "Directive"
                    self.addBuf(self.code[self.index])
                    self.getNext()
                elif self.code[self.index] == "}":
                    self.state = "Space"
                    self.addBuf(self.code[self.index])
                    self.lexes.pushLex(Token(coordinate, "Comment", self.buf, self.buf))
                    self.clearBuf()
                    self.getNext()
                else:
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Directive":
                if self.code[self.index] == "}":
                    self.state = "Space"
                    self.addBuf(self.code[self.index])
                    self.lexes.pushLex(Token(coordinate, "Directive", self.buf, self.buf))
                    self.clearBuf()
                    self.getNext()
                else:
                    self.addBuf(self.code[self.index])
                    self.getNext()

            elif self.state == "Separator":
                    self.state = "Space"
                    coordinate = self.index + 1

            elif self.state == "Assignment":
                self.state = "Space"
                if self.code[self.index] == '=':
                    self.addBuf(self.code[self.index])
                    self.getNext()
                self.lexes.pushLex(Token(coordinate, "Assignment", self.buf, self.buf))
                self.clearBuf()
                coordinate = self.index + 1

            elif self.state == "Error":
                if self.code[self.index] in self.space_symbols or self.code[self.index] == '.':
                    self.lexes.pushLex(Token(coordinate, "Error", self.buf, self.buf))
                    self.clearBuf()
                    self.state = "Final"
                else:
                    self.addBuf(self.code[self.index])
                    self.getNext()

    def getNext(self):
        self.index += 1

    def clearBuf(self):
        self.buf = ""

    def addBuf(self, buf):
        self.buf += buf

    def printLex(self):
        for lex in self.lexes.get_queue():
            print(lex.getParams())

    def getLex(self):
        return self.lexes.get_queue()