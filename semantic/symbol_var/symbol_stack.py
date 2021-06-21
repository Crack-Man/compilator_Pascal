class SymStack:
    def __init__(self):
        self.stack = []

    def push(self, sym_table):
        self.stack.append(sym_table)

    def pop(self):
        if self.stack:
            self.stack.pop(self.getCount() - 1)

    def top(self):
        if self.stack:
            return self.stack[self.getCount() - 1]

    def getCount(self):
        return len(self.stack)

    def getStack(self):
        return self.stack