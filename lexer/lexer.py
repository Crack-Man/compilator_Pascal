from lexer.token import Token

class Lexer:
    def __init__(self, path):
        self.path = path
        self.reserved = {"and", "array", "asm", "begin", "case", "const", "consatructor", "destructor", "div", "do",
                         "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                         "in", "inherited", "inline", "interface", "label", "library", "mod", "nil", "not", "object",
                         "of", "or", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                         "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor"}
        self.predefined = {"abs", "arctan", "boolean", "char", "chr", "cos", "dispose", "eoln", "exp",
                           "false", "get", "input", "integer", "ln", "maxint", "new", "odd", "ord", "output",
                           "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite", "round",
                           "sin", "sqr", "sqrt", "succ", "text", "true", "trunc", "unpack", "write", "writeln"}
        self.eof = {"eof"}
        self.admissible = {'.', ',', ':', ';', '(', ')', '[', ']', '+', '-', '*', '/', '=', '<', '>'}
        self.space_symbols = {' ', '\n', '\t', '\0', '\r'}
        self.operations = {'+', '-', '*', '/', '=', '<', '>', "**", ">=", "<="}
        self.composite_assignments = {"+=", "-=", "*=", "/="}
        self.separators = {'.', ',', ';', '(', ')', '[', ']', ".."}

        self.file = open(path, "r", encoding="utf-8")
        self.symbol = self.file.read(1)

        self.state = "Any"
        self.line = 1
        self.row = 1
        self.buf = ""
        self.coordinates = ""


    """
        Алгоритм идентификации лексемы построен на конечных автоматах.
        
        Начальное состояние - Any (любая возможная лексема). Any определяет, к какому состоянию следует перейти.
        Если встречен символ, который не соответствует текущему состоянию, осуществляется переход к состоянию Any,
        что позволяет избавиться от дублирования кода.
    """
    def findLexem(self):
        is_found = False
        token = Token()
        while not is_found:
            if self.state == "Any":
                if self.symbol in self.space_symbols:
                    if self.symbol == "\n":
                        self.newLine()
                    self.getNext()
                elif self.symbol.isalpha():
                    self.state = "Identifier"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol.isdigit():
                    self.state = "Integer"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == "'":
                    self.state = "Char"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol in self.operations:
                    self.state = "Operation"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == '{':
                    self.state = "Comment"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == ':':
                    self.state = "Assignment"
                    self.keepCoordinates()
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol in self.separators:
                    self.keepCoordinates()
                    self.state = "Separator"
                    self.addBuf(self.symbol)
                    self.getNext()
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Identifier":
                if self.symbol.isdigit() or self.symbol.isalpha():
                    self.addBuf(self.symbol)
                    if self.buf.lower() in self.eof:
                        self.state = "Final"
                        is_found = True
                    self.getNext()
                elif self.symbol in self.admissible or self.symbol in self.space_symbols:
                    self.state = "Any"
                    if self.buf.lower() in self.reserved:
                        token.setParams(self.coordinates, "Reserved Word", self.buf, self.buf)
                    elif self.buf.lower() in self.predefined:
                        token.setParams(self.coordinates, "Predefined Word", self.buf, self.buf)
                    else:
                        token.setParams(self.coordinates, "Identifier", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Integer":
                if self.symbol.isdigit():
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == ".":
                    self.state = "Real"
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol in self.admissible or self.symbol in self.space_symbols:
                    self.state = "Any"
                    token.setParams(self.coordinates, "Integer", self.buf, int(self.buf))
                    self.clearBuf()
                    is_found = True
                elif self.symbol.lower() == "e":
                    if self.buf.find('.') != len(self.buf) - 1:
                        self.state = "Real (Float Point): e"
                        self.addBuf(self.symbol)
                        self.getNext()
                    else:
                        self.state = "Error"
                        self.addBuf(self.symbol)
                        self.getNext()
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Real":
                admissible_real = self.admissible.copy()
                admissible_real.remove('.')
                if self.symbol.isdigit():
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol in admissible_real or self.symbol in self.space_symbols:
                    # Если буфер не оканчивается на точку, то выдаем лексему как вещественное число, иначе это ошибка
                    if self.buf.find('.') != len(self.buf) - 1:
                        self.state = "Any"
                        token.setParams(self.coordinates, "Real", self.buf, float(self.buf))
                        self.clearBuf()
                    else:
                        self.state = "Final"
                        token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    is_found = True
                elif self.symbol.lower() == "e":
                    if self.buf.find('.') != len(self.buf) - 1:
                        self.state = "Real (Float Point): e"
                        self.addBuf(self.symbol)
                        self.getNext()
                    else:
                        self.state = "Error"
                        self.addBuf(self.symbol)
                        self.getNext()
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Real (Float Point): e":
                if self.symbol == '+' or self.symbol == '-':
                    self.state = "Real (Float Point): octothorpe"
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol.isdigit():
                    self.state = "Real (Float Point): integer"
                    self.addBuf(self.symbol)
                    self.getNext()
                else:
                    self.state = "Final"
                    token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    is_found = True

            elif self.state == "Real (Float Point): octothorpe":
                if self.symbol.isdigit():
                    self.state = "Real (Float Point): integer"
                    self.addBuf(self.symbol)
                    self.getNext()
                else:
                    self.state = "Final"
                    token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    is_found = True

            elif self.state == "Real (Float Point): integer":
                if self.symbol.isdigit():
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol in self.admissible or self.symbol in self.space_symbols:
                    self.state = "Any"
                    token.setParams(self.coordinates, "Real", self.buf, float(self.buf))
                    self.clearBuf()
                    is_found = True
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()


            elif self.state == "Char":
                if self.symbol == '\n':
                    self.state = "Final"
                    token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                elif self.symbol != "'" and len(self.buf) == 2:
                    self.state = "String"
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol != "'":
                    self.addBuf(self.symbol)
                    self.getNext()
                else:
                    self.state = "Any"
                    self.addBuf(self.symbol)
                    token.setParams(self.coordinates, "Char", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                    self.getNext()

            elif self.state == "String":
                if self.symbol != "'" and self.symbol != '\n':
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == '\n':
                    self.state = "Final"
                    token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                else:
                    self.state = "Any"
                    self.addBuf(self.symbol)
                    token.setParams(self.coordinates, "String", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                    self.getNext()

            elif self.state == "Operation":
                if self.symbol in self.operations:
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == ' ' or self.symbol.isalpha() or self.symbol.isdigit():
                    if self.buf in self.operations:
                        self.state = "Any"
                        token.setParams(self.coordinates, "Operation", self.buf, self.buf)
                        self.clearBuf()
                        is_found = True
                    elif self.buf in self.composite_assignments:
                        self.state = "Any"
                        token.setParams(self.coordinates, "Assignment", self.buf, self.buf)
                        self.clearBuf()
                        is_found = True
                    else:
                        self.state = "Error"
                        self.addBuf(self.symbol)
                        self.getNext()
                else:
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Comment":
                if self.symbol == "$" and len(self.buf) == 1:
                    self.state = "Directive"
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == "\n":
                    self.addBuf(self.symbol)
                    self.newLine()
                    self.getNext()
                elif self.symbol == "}":
                    self.state = "Any"
                    self.clearBuf()
                    self.getNext()
                elif self.buf.find("eof") != -1:
                    self.state = "Final"
                    token.setParams(
                        self.coordinates, "Error",
                        self.buf.replace(" eof", "").encode("unicode_escape").decode("utf-8"),
                        self.buf.replace(" eof", "").encode("unicode_escape").decode("utf-8")
                    )
                    self.clearBuf()
                    is_found = True
                else:
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Directive":
                if self.symbol == "}":
                    self.state = "Any"
                    self.addBuf(self.symbol)
                    token.setParams(self.coordinates, "Directive", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                    self.getNext()
                elif self.symbol == "\n":
                    self.addBuf(self.symbol)
                    self.newLine()
                    self.getNext()
                elif self.buf.find("eof") != -1:
                    self.state = "Final"
                    token.setParams(
                        self.coordinates, "Error",
                        self.buf.replace(" eof", "").encode("unicode_escape").decode("utf-8"),
                        self.buf.replace(" eof", "").encode("unicode_escape").decode("utf-8")
                    )
                    self.clearBuf()
                    is_found = True
                else:
                    self.addBuf(self.symbol)
                    self.getNext()

            elif self.state == "Separator":
                self.state = "Any"
                if self.symbol.isdigit() and self.buf == '.':
                    self.state = "Error"
                    self.addBuf(self.symbol)
                    self.getNext()
                elif self.symbol == '.':
                    self.addBuf(self.symbol)
                    self.getNext()
                    token.setParams(self.coordinates, "Separator", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True
                else:
                    token.setParams(self.coordinates, "Separator", self.buf, self.buf)
                    self.clearBuf()
                    is_found = True

            elif self.state == "Assignment":
                self.state = "Any"
                if self.symbol == '=':
                    self.addBuf(self.symbol)
                token.setParams(self.coordinates, "Assignment", self.buf, self.buf)
                self.clearBuf()
                is_found = True
                self.getNext()

            elif self.state == "Error":
                if self.symbol in self.space_symbols or self.symbol == '.':
                    token.setParams(self.coordinates, "Error", self.buf, self.buf)
                    self.clearBuf()
                    self.state = "Final"
                    is_found = True
                else:
                    self.addBuf(self.symbol)
                    self.getNext()
        return token

    def notEOF(self):
        return self.state != "Final"

    def newLine(self):
        self.line += 1
        self.row = 0

    def keepCoordinates(self):
        self.coordinates = "{}:{}".format(self.line, self.row)

    def getNext(self):
        self.symbol = self.file.read(1)
        self.row += 1

    def clearBuf(self):
        self.buf = ""

    def addBuf(self, buf):
        self.buf += buf