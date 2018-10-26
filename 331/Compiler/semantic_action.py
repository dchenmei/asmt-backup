from symbol_table import *
from error import SemanticActionError

class SemanticAction:
    def __init__(self):
        self.stack = []
        # these are assumed to be private (i.e. do not call them outside of the class!)
        self.insert = True # True = insert mode, False = search mode
        self.global_env = True # True = Global, False = local
        self.is_array = False # True = array, False = simple variable
        self.global_mem = 0
        self.local_mem = 0

        # TODO: more specific capacity later, if needed
        self.local_table = SymbolTable(100000)
        self.global_table = SymbolTable(100000)

    def execute(self, action_num, token):
        if action_num == 1:
            self.insert = True
        elif action_num == 2:
            self.insert = False
        elif action_num == 3:
           self.action_3()
        elif action_num == 4:
            self.action_4(token)
        elif action_num == 6:
            self.is_array = True
        elif action_num == 7:
            self.action_7(token)
        elif action_num == 9:
            self.action_9()
        elif action_num == 13:
            self.action_13(token)
        else:
            # TODO: in the future, when valid numbers are implemented, raise error
            print("Action number invalid or currently not supported.")

    def action_3(self):
        type = self.stack.pop().type()
        if self.is_array:
            upper_bound = int(self.stack.pop().value())
            lower_bound = int(self.stack.pop().value())
            mem_size = (upper_bound - lower_bound) + 1

            while self.stack and self.stack[-1].type() == "IDENTIFIER":
                tok = self.stack.pop()
                id = ArrayEntry(tok.value(), 0, type, upper_bound, lower_bound)

                if self.global_env:
                    id.address = self.global_mem
                    self.global_table.insert(tok.value(), id)
                    self.global_mem += mem_size
                else:
                    id.address = self.local_mem
                    self.local_table.insert(tok.value(), id)
                    self.local_mem += mem_size
        else:
            while self.stack and self.stack[-1].type() == "IDENTIFIER":
                tok = self.stack.pop()
                id = ArrayEntry(tok.value(), 0, type, 0, 0)
                if self.global_env:
                    id.address = self.global_mem
                    self.global_table.insert(tok.value(), id)
                    self.global_mem += 1
                else:
                    id.address = self.local_mem
                    self.local_table.insert(tok.value(), id)
                    self.local_mem += 1

        self.is_array = False

    def action_4(self, token):
        # Only possible types passing through here are either integer or real
        if token.type() != "INTEGER" and token.type() != "REAL":
            raise SemanticActionError("expected type of integer or real", token.line())
        else:
            self.stack.append(token)

    def action_7(self, token):
        if token.type() == "INTCONSTANT":
            self.stack.append(token)
        else:
            raise SemanticActionError("expected integer constant", token.line())

    def action_9(self):
        if len(self.stack) < 3 or \
            self.stack[-1].type() != "IDENTIFIER" or \
            self.stack[-2].type() != "IDENTIFIER" or \
            self.stack[-3].type() != "IDENTIFIER":
                raise SemanticActionError("expected three identifiers", token.line())

        id1 = self.stack.pop()
        id2 = self.stack.pop()
        id3 = self.stack.pop()

        io_entry1 = IODeviceEntry(id1.value())
        io_entry2 = IODeviceEntry(id2.value())
        procedure_entry = ProcedureEntry(id3.value(), 0, None)

        io_entry1.reserved = True
        io_entry2.reserved = True
        procedure_entry.reserved = True

        self.global_table.insert(id1.value(), io_entry1)
        self.global_table.insert(id2.value(), io_entry2)
        self.global_table.insert(id3.value(), procedure_entry)

        self.insert = False

    def action_13(self, token):
        if token.type() == "IDENTIFIER":
            self.stack.append(token)
        else:
            raise SemanticActionError("expected identifier", token.line())

    def dump(self):
        out = "Stack ::==>"
        if len(self.stack) == 0:
            print(out)

        for token in list(reversed(self.stack)):
            out += " " + token.str() + ","

        print(out[:-1]) # kind of a hackish way to get rid of the extra comma, can also use if
