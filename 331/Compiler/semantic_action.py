from symbol_table import *

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
        self.global_table = SymbolTable(100000)

    def execute(self, action_num, token):
        # TODO: maybe if statements is okay for now but there gotta be a better way
        # Plus it grows larger so functions are a no brainer here
        if action_num == 1:
            self.insert = True
        elif action_num == 2:
            self.insert = False
        elif action_num == 4:
            # TODO: how to check if it is a type?
            self.stack.append(token)
        elif action_num == 7:
            # TODO: how to check if it is an integer identifier?
            self.stack.append(token)
        elif action_num == 6:
            self.is_array = True
        elif action_num == 9:
            # TODO: how do you know you will get exactly 3 well behaving from stack
            id1 = self.stack.pop()
            id2 = self.stack.pop()
            id3 = self.stack.pop()

            io_entry1 = IODeviceEntry(id1)
            io_entry2 = IODeviceEntry(id2)
            procedure_entry = ProcedureEntry(id3, 0, None)
            self.global_table.insert(id1.value(), io_entry1)
            self.global_table.insert(id2.value(), io_entry2)
            self.global_table.insert(id3.value(), procedure_entry)

            self.insert = False

        elif action_num == 13:
            # TODO: check identifier type
            self.stack.append(token)
        else:
            print("Action number invalid or currently not supported.")


        print("ACTION", action_num, "TOKEN", token.type())

    def dump(self):
        print("Stack ::==>", list(reversed(self.stack)))

if __name__ == '__main__':
    print("HELLO WORLD, ONCE AGAIN")
    action = SemanticAction()