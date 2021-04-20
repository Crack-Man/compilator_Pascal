from lexer.token import Token
from enum import Enum

class States(Enum):
    any = "Any"
    reserved = "Reserved Word"
    predefined = "Predefined Word"
    identifier = "Identifier"
    integer = "Integer"
    real = "Real"
    real_e = "Real (Float Point): e"
    real_plus_minus = "Real (Float Point): plus-minus"
    real_degree = "Real (Float Point): degree"
    string = "String"
    operation = "Operation"
    separator = "Separator"
    assignment = "Assignment"
    comment = "Comment"
    directive = "Directive"
    error = "Error"

class Lexer:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path, "r", encoding="utf-8")
        self.symbol = self.file.read(1)

        self.reserved = {"and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "nil", "not", "object",
                         "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}
        # predefined - предописанные слова
        self.predefined = {"abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eof", "eoln", "exp",
                           "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                           "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                           "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}
        self.space_symbols = {'', ' ', '\n', '\t', '\0', '\r'}
        self.operations = {'+', '-', '*', '/', '=', '<', '>', "div", "mod"}
        self.operations_arr = {'+', '-', '*', '/'}
        self.operations_bool = {'>', '<'}
        self.assignments = {":=", "+=", "-=", "*=", "/="}
        self.separators = {'.', ',', ':', ';', '(', ')', '[', ']', ".."}

        self.state = States.any
        self.line, self.col = 1, 1
        self.buf, self.unget, self.coordinates = "", "", ""

    def getLexem(self):
        self.clearBuf()
        while self.symbol or self.buf:
            if self.state == States.any:
                if self.symbol in self.space_symbols:
                    if self.symbol == "\n":
                        self.newLine()
                    self.getSymbol()
                elif self.symbol.isalpha():
                    self.keepSymbol(state=States.identifier, keep_coordinates=True)
                elif self.symbol.isdigit():
                    self.keepSymbol(state=States.integer, keep_coordinates=True)
                elif self.symbol == "'":
                    self.keepSymbol(state=States.string, keep_coordinates=True)
                elif self.symbol in self.operations:
                    self.keepSymbol(state=States.operation, keep_coordinates=True)
                elif self.symbol == '{':
                    self.keepSymbol(state=States.comment, keep_coordinates=True)
                elif self.symbol in self.separators:
                    self.keepSymbol(state=States.separator, keep_coordinates=True)
                else:
                    self.keepSymbol(state=States.error, keep_coordinates=True)

            elif self.state == States.identifier:
                if self.symbol.isdigit() or self.symbol.isalpha() or self.symbol == "_":
                    self.keepSymbol()
                else:
                    self.state = States.any
                    type_lexem = States.identifier.value
                    if self.buf.lower() in self.reserved:
                        type_lexem = States.reserved.value
                    elif self.buf.lower() in self.predefined:
                        type_lexem = States.predefined.value
                    elif self.buf.lower() in self.operations:
                        type_lexem = States.operation.value
                    return Token(self.coordinates, type_lexem, self.buf, self.buf)

            elif self.state == States.integer:
                if self.symbol.isdigit():
                    self.keepSymbol()
                elif self.symbol == ".":
                    self.state = States.real
                    self.keepSymbol()
                elif self.symbol.lower() == "e":
                    self.state = States.real_e
                    self.keepSymbol()
                elif self.symbol.isalpha():
                    self.state = States.error
                    self.keepSymbol()
                else:
                    self.state = States.any
                    if -32768 <= int(self.buf) <= 32767:
                        return Token(self.coordinates, States.integer.value, self.buf, int(self.buf))
                    else:
                        self.informError(
                            f"{self.path}        {self.coordinates}        "
                            f"Range check error while evaluating constants ({self.buf})\n"
                        )

            elif self.state == States.real:
                if self.symbol.isdigit():
                    self.keepSymbol()
                elif self.symbol.lower() == "e":
                    if self.buf[len(self.buf) - 1] != '.':
                        self.state = States.real_e
                        self.keepSymbol()
                    else:
                        self.state = States.error
                        self.keepSymbol()
                elif self.symbol == '.' and self.buf[len(self.buf) - 1] == '.':
                    self.state = States.any
                    self.buf = self.buf[:len(self.buf) - 1]
                    self.setUnget(".")
                    return Token(self.coordinates, States.integer.value, self.buf, int(self.buf))
                else:
                    if self.buf[len(self.buf) - 1] != '.':
                        self.state = States.any
                        if 2.9e-39 <= float(self.buf) <= 1.7e38:
                            return Token(self.coordinates, States.real.value, self.buf, float(self.buf))
                        else:
                            self.informError(
                                f"{self.path}        {self.coordinates}        "
                                f"Range check error while evaluating constants ({self.buf})\n"
                            )
                    else:
                        self.state = States.error
                        self.keepSymbol()

            elif self.state == States.real_e:
                if self.symbol == '+' or self.symbol == '-' or self.symbol.isdigit():
                    self.state = States.real_degree if self.symbol.isdigit()\
                        else States.real_plus_minus
                    self.keepSymbol()
                else:
                    self.state = States.error
                    self.keepSymbol()

            elif self.state == States.real_plus_minus:
                if self.symbol.isdigit():
                    self.state = States.real_degree
                    self.addBuf()
                    self.getSymbol()
                else:
                    self.state = States.error
                    self.keepSymbol()

            elif self.state == States.real_degree:
                if self.symbol.isdigit():
                    self.keepSymbol()
                else:
                    self.state = States.any
                    if 2.9e-39 <= float(self.buf) <= 1.7e38:
                        return Token(self.coordinates, States.real.value, self.buf, float(self.buf))
                    else:
                        self.informError(
                            f"{self.path}        {self.coordinates}        "
                            f"Range check error while evaluating constants ({self.buf})\n"
                        )

            elif self.state == States.string:
                if self.symbol == '\n':
                    self.state = States.error
                elif self.symbol == '':
                    self.informError(
                        f'{self.path}        {self.line}:{self.col}        '
                        f'End of file was encountered, but "\'" was expected in "{self.buf}"\n'
                    )
                elif self.symbol != "'":
                    self.keepSymbol()
                else:
                    self.state = States.any
                    self.keepSymbol()
                    return Token(self.coordinates, States.string.value, self.buf, self.buf)

            elif self.state == States.operation:
                if (self.buf in self.operations_arr or self.buf in self.operations_bool) and self.symbol == '=' \
                    or self.buf == '*' and self.symbol == '*':
                        self.keepSymbol()
                else:
                    self.state = States.any
                    type_lexem = States.assignment.value if self.buf in self.assignments else States.operation.value
                    return Token(self.coordinates, type_lexem, self.buf, self.buf)

            elif self.state == States.separator:
                self.state = States.any
                type_lexem = States.separator.value
                if self.buf == '.' and self.symbol == '.' or self.buf == ':' and self.symbol == '=':
                    self.addBuf()
                    if self.buf == ":=":
                        type_lexem = States.assignment.value
                    self.getSymbol()
                    return Token(self.coordinates, type_lexem, self.buf, self.buf)
                elif self.buf == '.':
                    if self.symbol in self.space_symbols:
                        return Token(self.coordinates, type_lexem, self.buf, self.buf)
                    else:
                        self.state = States.error
                        self.keepSymbol()
                else:
                    return Token(self.coordinates, type_lexem, self.buf, self.buf)

            elif self.state == States.comment:
                if self.symbol == "$" and len(self.buf) == 1:
                    self.state = States.directive
                    self.keepSymbol()
                elif self.symbol == "\n":
                    self.addBuf()
                    self.newLine()
                    self.getSymbol()
                elif self.symbol == "}":
                    self.state = States.any
                    self.clearBuf()
                    self.getSymbol()
                elif self.symbol == '':
                    self.buf = self.buf.encode("unicode_escape").decode("utf-8")
                    self.informError(
                        f'{self.path}        {self.line}:{self.col}        ' +
                        'End of file was encountered, but "}" ' +
                        f'was expected in "{self.buf}"\n'
                    )
                else:
                    self.keepSymbol()

            elif self.state == States.directive:
                if self.symbol == "\n":
                    self.addBuf()
                    self.newLine()
                    self.getSymbol()
                elif self.symbol == "}":
                    self.state = States.any
                    self.keepSymbol()
                    return Token(self.coordinates, States.directive.value, self.buf, self.buf)
                else:
                    self.keepSymbol()

            elif self.state == States.error:
                if self.symbol in self.space_symbols or self.symbol in self.separators:
                    self.informError(f'{self.path}        {self.coordinates}        Unexpected word "{self.buf}"\n')
                else:
                    self.keepSymbol()
        return Token("", "EOF", "", "")

    def informError(self, text):
        self.error_lexem = Token(self.coordinates, States.error.value, self.buf, self.buf)
        raise RuntimeError(text)

    def getErrorLexem(self):
        return self.error_lexem

    def keepSymbol(self, **kwargs):
        if 'state' in kwargs:
            self.state = kwargs['state']
        if 'keep_coordinates' in kwargs:
            if kwargs['keep_coordinates']:
                self.keepCoordinates()
        self.addBuf()
        self.getSymbol()

    def keepCoordinates(self):
        self.coordinates = f"{self.line}:{self.col}"

    def getSymbol(self):
        if self.unget:
            self.symbol = self.unget
            self.unget = ""
        else:
            self.symbol = self.file.read(1)
        self.col += 1

    def newLine(self):
        self.line += 1
        self.col = 0

    def setUnget(self, value):
        self.unget = value
        self.col -= 1

    def clearBuf(self):
        self.buf = ""

    def addBuf(self):
        self.buf += self.symbol