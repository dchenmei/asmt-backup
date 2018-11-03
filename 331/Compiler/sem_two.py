from symbol_table import *
from quadruples import Quadruples
from error import SemanticActionError

class SemanticAction:

    #*****************************************************#
    # Helper Functions                                    #
    #*****************************************************#

    def type_check(self, id1, id2):
        t1 = id1.type
        t2 = id2.type

        if t1 == "INTEGER" and t2 == "INTEGER":
            return 0
        elif t1 == "REAL" and t2 == "REAL":
            return 1
        elif t1 == "REAL" and t2 == "INTEGER":
            return 2
        elif t1 == "INTEGER" and t2 == "REAL":
            return 3

    def get_entry_prefix(self, entry):
        if self.global_env or self.local_table.find(entry.name) is None:
            return "_"
        else: # local
            return "%"

    def get_entry_addr(self, entry):
        if entry.is_variable() or entry.is_array():
            return abs(entry.address)
        elif entry.is_constant():
            tmp = self.create("tmp", entry.type)
            self.generate("move", entry.name, tmp)
            return abs(tmp.address)

    def generate(self, op, id1=None, id2=None, id3=None):
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
            quad.append(self.get_entry_prefix(id2) + str(self.get_entry_addr(id2)))
        else:
            quad.append(id2) # append None

        if type(id3) is str or type(id3) is int:
            quad.append(str(id3))
        elif id3:
            quad.append(self.get_entry_prefix(id3) + str(self.get_entry_addr(id3)))
        else:
            quad.append(id3) # append None

        self.quads.add_quad(quad)

    def create(self, name, type):
        ve = VariableEntry(name, 0, type)

        if self.global_env:
            ve.address = -1 * self.global_mem
            self.global_mem += 1
            self.global_table.insert(name + str(self.tmp_id), ve) # append id to make each tmp unique
        else:
            ve.address = -1 * self.local_mem
            self.local_mem += 1
            self.local_table.insert(name + str(self.tmp_id), ve)

        self.tmp_id += 1
        return ve

    def backpatch(self, quad_idx, x):
        self.quads.set_field(quad_idx, 1, x) # assume quadruples are 0 indexed so 2nd field is at index 1

    # Note: expects id as a string
    def lookup(self, id):
        entry = self.local_table.find(id)
        if not entry:
            entry = self.global_table.find(id)

        return entry

    #*****************************************************#
    # Initialization and Entry Point (execute)            #
    #*****************************************************#

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

        # reserved words
        main = ProcedureEntry("MAIN", 0, None)
        read = ProcedureEntry("READ", 0, None)
        write = ProcedureEntry("WRITE", 0, None)

        main.reserved = True
        read.reserved = True
        write.reserved = True

        self.global_table.insert(main.name, main)
        self.global_table.insert(read.name, read)
        self.global_table.insert(write.name, write)

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
            id = self.lookup(token.value())
            if not id:
                raise SemanticActionError("undeclared variable", token.line())
            print(id.name)
            self.stack.append(id)
        elif action_num == 31:
            self.action_31(token)
        elif action_num == 40:
            if token.type() != "UNARYPLUS" and token.type() != "UNARYMINUS":
                raise SemanticActionError("expected uplus or uminus", token.line())
            self.stack.append(token)
        elif action_num == 41:
            self.action_41(token)
        elif action_num == 42:
            if token.type()[-2:] != "OP":
                raise SemanticActionError("expected an operator", token.line())

            self.stack.append(token)
        elif action_num == 43:
            self.action_43(token)
        elif action_num == 44:
            if token.type()[-2:] != "OP":
                raise SemanticActionError("expected an operator", token.line())

            self.stack.append(token)
        elif action_num == 45:
            self.action_45(token)
        elif action_num == 46:
            self.action_46(token)
        elif action_num == 48:
            self.action_48(token)
        elif action_num == 55:
            self.backpatch(self.global_store, self.global_mem)
            self.generate("free", self.global_mem)
            self.generate("PROCEND")
        elif action_num == 56:
             self.generate("PROCBEGIN", "main")
             self.global_store = self.quads.get_next_quad()
             self.generate("alloc", "_")
        else:
            # TODO: in the future, when valid numbers are implemented, raise error
            print("Action number invalid or currently not supported.")

        #self.quads.print()
        #self.dump()

    #*****************************************************#
    # Implementations of Individual Actions               #
    #*****************************************************#

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
                    id.address = -1 * self.local_mem # negative to distinguish temporary variables
                    self.local_table.insert(tok.value(), id)
                    self.local_mem += mem_size
        else:
            while self.stack and self.stack[-1].type() == "IDENTIFIER":
                tok = self.stack.pop()
                id = VariableEntry(tok.value(), 0, type)
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
        id2 = self.stack.pop()
        offset = None
        id1 = self.stack.pop()

        check = self.type_check(id1, id2)
        if check == 3:
            raise SemanticActionError("type mismatch", token.line())

        if check == 2:
            tmp = self.create("tmp", id1.type)
            self.generate("ltof", id2, tmp)
            if offset is None:
                self.generate("move", tmp, id1)
            else:
                self.generate("stor", tmp, offset, id1)
        else:
            if offset is None:
                self.generate("move", id2, id1)
            else:
                self.generate("stor", id2, offset, id1)

    def action_41(self, token):
        id = self.stack.pop()
        sign = stack.pop()
        if sign.type == "UNARYMINUS":
            id_type = id.type
            tmp = self.create("tmp", id_type)
            if id_type == "INTEGER":
                self.generate("uminus", id, tmp)
            else:
                self.generate("fuminus", id, tmp)

            self.stack.append(tmp)
        else:
            self.stack.append(id)

    def action_43(self, toggken):
        id2 = self.stack.pop()
        op = self.stack.pop()
        id1 = self.stack.pop()
        opcode = op.op_code()

        check = self.type_check(id1, id2)
        if check == 0:
            tmp = self.create("tmp", "INTEGER")
            self.generate(opcode, id1, id2, tmp)
            self.stack.append(tmp)
        elif check == 1:
            tmp = self.create("tmp", "REAL")
            self.generate("f" + opcode, id1, id2, tmp)
            self.stack.append(tmp)
        elif check == 2:
            tmp1 = self.create("tmp", "REAL")
            tmp2 = self.create("tmp", "REAL")
            self.generate("ltof", id2, tmp1)
            self.generate("f" + opcode, id1, tmp1, tmp2)
            self.stack.append(tmp2)
        elif check == 3:
            tmp1 = self.create("tmp", "REAL")
            tmp2 = self.create("tmp", "REAL")
            self.generate("ltof", id1, tmp1)
            self.generate("f" + opcode, tmp1, id2, tmp2)
            self.stack.append(tmp2)

    def action_45(self, token):
        id2 = self.stack.pop()
        op = self.stack.pop()
        id1 = self.stack.pop()
        opcode = op.op_code()

        check = self.type_check(id1, id2)
        if check != 0 and (op.is_div() or op.is_mod()):
            # Only integers are valid operand for DIV and MOD
            raise SemanticActionError("bad parameter, expected type integer", token.line())

        if check == 0:
            # Assume MULOPS
            if op.is_mod():
                tmp1 = self.create("tmp", "INTEGER")
                tmp2 = self.create("tmp", "INTEGER")
                tmp3 = self.create("tmp", "INTEGER")
                self.generate("div", id1, id2, tmp1)
                self.generate("mul", id2, tmp1, tmp2)
                self.generate("sub", id1, tmp2, tmp3)
                self.stack.append(tmp3)
            elif op.value() == 2: # /
                tmp1 = self.create("tmp", "REAL")
                tmp2 = self.create("tmp", "REAL")
                tmp3 = self.create("tmp", "REAL")
                self.generate("ltof", id1, tmp1)
                self.generate("ltof", id2, tmp2)
                self.generate("fdiv", tmp1, tmp2, tmp3)
                self.stack.append(tmp3)
            else:
                tmp = self.create("tmp", "INTEGER")
                self.generate(opcode, id1, id2, tmp)
                self.stack.append(tmp)
        elif check == 1:
            tmp = self.create("tmp", "REAL")
            self.generate("f" + opcode, id1, id2, tmp)
            self.stack.append(tmp)
        elif check == 2:
            tmp1 = self.create("tmp", "REAL")
            tmp2 = self.create("tmp", "REAL")
            self.generate("ltof", id2, tmp1)
            self.generate("f" + opcode, id1, tmp1, tmp2)
            self.stack.append(tmp2)
        elif check == 3:
            tmp1 = self.create("tmp", "REAL")
            tmp2 = self.create("tmp", "REAL")
            self.generate("ltof", id1, tmp1)
            self.generate("f" + opcode, tmp1, id2, tmp2)
            self.stack.append(tmp2)

    def action_46(self, token):
        if token.type() == "IDENTIFIER":
            id = self.lookup(token.value())
            if id is None:
                raise SemanticActionError("undeclared variable", token.line())

            self.stack.append(id)

        elif token.type() == "INTCONSTANT" or token.type() == "REALCONSTANT":
            id = self.lookup(token.value())
            if id is None:
                if (token.type() == "INTCONSTANT"):
                    id = ConstantEntry(token.value(), "INTEGER")
                elif (token.type() == "REALCONSTANT"):
                    id = ConstantEntry(token.value(), "REAL")

                self.constant_table.insert(id.name, id)

            self.stack.append(id)


    def action_48(self, token):
        offset = None
        if offset:
            id = self.stack.pop()
            tmp = self.create("tmp", id.type)
            self.generate("load", id, offset, tmp)
            self.stack.append(tmp)

    def dump(self):
        out = "Stack ::==>"
        if len(self.stack) == 0:
            print(out)

        for token in list(reversed(self.stack)):
            out += " " + str(type(token)) + ","

        print(out[:-1]) # rid of the dangling comma

    def dump_tvi(self):
        self.quads.print()