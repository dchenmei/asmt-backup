from symbol_table import *
from error import SemanticActionError

class SemanticAction:
    def __init__(self):
        self.stack = []
        # these are assumed to be private (i.e. don't call them outside of the class!)
        self.insert = True # True = insert mode, False = search mode
        self.global_env = True # True = Global, False = local
        self.is_array = True # True = array, False = simple variable
        self.global_mem = 0
        self.local_mem = 0

        # TODO: what is the capacity?
        self.local_table = SymbolTable(100000)
        self.global_table = SymbolTable(100000)

    def execute(self, action_num, token):
        # TODO: maybe if statements is okay for now but there gotta be a better way
        # Plus it grows larger so functions are a no brainer here
        if action_num == 1:
            self.insert = True
        elif action_num == 2:
            self.insert = False
        elif action_num == 3:
            self.action_3()
        elif action_num == 4:
            self.action_4(token);
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

        print("ACTION", action_num, "TOKEN", token.type())

    def action_3(self):
        type = self.stack.pop().type()
        if type == "ARRAY":
            upper_bound = stack.pop()
            lower_bound = stack.pop()
            mem_size = (upper_bound - lower_bound) + 1

            while self.stack[-1].type() == "IDENTIFIER":
                tok = stack.pop()
                id = ArrayEntry(tok.value(), 0, type, upper_bound, lower_bound)

            if self.global_env:
                id.address = self.global_mem
                # TODO : insert into global table
                global_mem += mem_size
            else:
                id.address = self.local_mem
                # TODO : insert into local table
                local_mem += mem_size

    def action_4(self, token):
        # TODO: how the heck do you check the type when you only have token and don't know what types are allowed
        if False:
            raise SemanticActionError("expected type", 0, 0)
        else:
            self.stack.append(token)

    def action_7(self, token):
        # Must be int constant
        if token.type() == "INTCONSTANT":
            self.stack.append(token)
        else:
            raise SemanticActionError("expected integer constant", 0, 0)

    def action_9(self):
        # TODO: probably not likely and also check if the three it contains are identifiers
        if self.stack.size() < 3
            raise SemanticActionError("expected identifiers", 0, 0)
        id1 = self.stack.pop()
        id2 = self.stack.pop()
        id3 = self.stack.pop()

        # TODO: set all reversed to true
        io_entry1 = IODeviceEntry(id1)
        io_entry2 = IODeviceEntry(id2)
        procedure_entry = ProcedureEntry(id3, 0, None)
        self.global_table.insert(id1.value(), io_entry1)
        self.global_table.insert(id2.value(), io_entry2)
        self.global_table.insert(id3.value(), procedure_entry)

        self.insert = False

    def action_13(self, token):
        if token.type() == "IDENTIFIER":
            self.stack.append(token)
        else:
            raise SemanticActionError("expected identifier", 0, 0)

    def dump(self):
        print("Stack ::==>", list(reversed(self.stack)))

if __name__ == '__main__':
    print("HELLO WORLD, ONCE AGAIN")
    action = SemanticAction()