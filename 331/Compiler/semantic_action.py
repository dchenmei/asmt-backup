from symbol_table import *
from quadruples import Quadruples
from error import SemanticActionError

# TODO: should helper functions be part of the class, probably, we will see
# put in self as part of the parameters if they are going into the class!!!!
# these are identifiers folk, don't be fooled
def type_check(x, y):
    # Implemention is concise, chart for reference
    # int int   -> 0
    # real real -> 1
    # real int  -> 2
    # int real  -> 3
    # TODO: can we nicely assume that the only two possible type passed in here are int and real
    x = x.type()
    y = y.type()
    if x == y:
        return int(x == "REAL") # TODO: will they be passed in as "INTEGER" or "int"
    else:
        return int(y == "REAL") + 2

class SemanticAction:
    def __init__(self):
        self.stack = []
        # these are assumed to be private (i.e. do not call them outside of the class!)
        self.insert = True # True = insert mode, False = search mode
        self.global_env = True # True = Global, False = local
        self.is_array = False # True = array, False = simple variable
        self.global_mem = 0
        self.local_mem = 0
        self.global_store = 0
        self.tmp_id = 0 # id for temporary variable generated with create()
        self.quads = Quadruples()

        # TODO: more specific capacity later, if needed
        self.local_table = SymbolTable(100000)
        self.constant_table = SymbolTable(100000)
        self.global_table = SymbolTable(100000)

        # reserved words: MAIN, READ, WRITE
        main = ProcedureEntry("MAIN", 0, None)
        read = ProcedureEntry("READ", 0, None)
        write = ProcedureEntry("WRITE", 0, None)

        main.reserved = True
        read.reserved = True
        write.reserved = True

        self.global_table.insert(main.name, main)
        self.global_table.insert(read.name, read)
        self.global_table.insert(write.name, write)

    def get_entry_prefix(self, entry):
        addr = entry.address

        # is vs == ?
        #  maybe we shouldnt touch member variables lke this
        # maybe it can be negative and end up in global like a global temp
        if addr > 0 or self.local_table.find(entry.name) is None: # global
            return "_"
        else: # local
            return "%"

    def get_entry_addr(self, entry):
        # TODO: refactor to not use camel case please
        if entry.isVariable() or entry.isArray():
            return entry.address
        else: # assume  is constant, there is no isConstant function?
            tmp = self.create("tmp", entry.type)
            generate("move", entry.name, tmp)
            return tmp.address

    # not using *args, because that is overkill
    # what kind of args come in here, id or addresses
    # just to clarify, what is passed here are entry types
    # what is passed in here is very ambiguous, it can be an entry but sometimes string or #s
    def generate(self, op, id1=None, id2=None, id3=None):
        # TODO: most likely a better idea if we write an overriden function but this will do for now

        quad = []
        quad.append(op)

        if type(id1) is str or type(id1) is int:
            quad.append(str(id1))
        elif id1:
            quad.append(self.get_entry_prefix(id1) + str(self.get_entry_addr(id1)))
        else:
            quad.append(id1) # append None

        if type(id2) is str or type(id2) is int:
            quad.append(str(id2))
        elif id2:
            quad.append(self.get_entry_prefix(id2) + self.get_entry_addr(id2))
        else:
            quad.append(id2) # append None

        if type(id3) is str or type(id3) is int:
            quad.append(str(id3))
        elif id3:
            quad.append(self.get_entry_prefix(id3) + self.get_entry_addr(id3))
        else:
            quad.append(id3) # append None

        self.quads.add_quad(quad)

    def create(self, name, type):
        # TODO: do we need to append the id here too?
        ve = VariableEntry(name, 0, type)

        # temporary variable, -1 to distinguish (what if it ends up in the global table, SMELLS LIKE A BUG)
        if self.global_env:
            ve.address = -1 * self.global_mem
            self.global_mem += 1
            self.global_table.insert(name + str(self.tmp_id), ve) # append id to make each tmp unique
        else:
            ve.address = -1 * self.local_mem
            self.local_mem += 1
            self.local_table.insert(name + str(self.tmp_id), ve)

        tmp_id += 1
        return ve

    def backpatch(self, quad_idx, x):
        self.quads.set_field(quad_idx, 1, x) # assume the quadruples are 0 indexed so 2nd is index 1

    # TODO: we need to clarify what is passed where because there is a heap of confusion here
    def lookup(self, id):
        entry = self.local_table.find(id.value())
        if not entry:
            entry = self.global_table.find(id.value())

        return entry

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
        elif action_num == 30:
            id = self.lookup(token)
            if not id:
                raise SemanticActionError("undeclared variable", token.line())
            self.stack.append(id)
        elif action_num == 31:
            self.action_31(token) # Don't think we need to pass in a token
        elif action_num == 40:
            if token.type() != "UNARYPLUS" and token.type() != "UNARYMINUS":
                raise SemanticActionError("expected uplus or uminus", token.line())

            self.stack.append(token)
        elif action_num == 42:
            # oh jeez, so hackish
            if token.type()[-2:] != "OP":
                raise SemanticActionError("expected an operator", token.line())

            self.stack.append(token)
        elif action_num == 44:
            # oh jeez, so hackish
            if token.type()[-2:] != "OP":
                raise SemanticActionError("expected an operator", token.line())

            self.stack.append(token)
        elif action_num == 55:
            self.backpatch(self.global_store, self.global_mem)
            self.generate("free", self.global_mem)
            self.generate("procend")
        elif action_num == 56:
             self.generate("procbegin", "main")
             self.global_store = self.quads.get_next_quad()
             self.generate("alloc", "_")
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
                    id.address = -1 * self.local_mem # negative to distinguish from global entries
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

        self.generate("call", "main", "0")
        self.generate("exit")

    def action_13(self, token):
        if token.type() == "IDENTIFIER":
            self.stack.append(token)
        else:
            raise SemanticActionError("expected identifier", token.line())

    def action_31(self, token):
        self.dump()
        # TODO: make sure you check for empty list errors when popping anything
        # these are all entry types
        id2 = self.stack.pop()
        offset = None
        id1 = self.stack.pop()

        if typecheck(id1, id2) == 3:
            raise SemanticActionError("type mismatch", token.line()) # which line should we use?
        if typecheck(id1, id2) == 2:
            tmp = self.create("tmp", id1.type()) # id1 is a real here?

    def dump(self):
        out = "Stack ::==>"
        if len(self.stack) == 0:
            print(out)

        # TODO: Stack has token and entries???
        for token in list(reversed(self.stack)):
            out += " " + token.str() + ","

        print(out[:-1]) # kind of a hackish way to get rid of the extra comma, can also use if