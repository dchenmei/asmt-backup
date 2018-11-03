from error import SymbolTableError

class SymbolTable:

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.hashtable = {}

    def find(self, key):
        key = key.upper()
        if key not in self.hashtable:
            return None
        else:
            return self.hashtable[key]

    def insert(self, key, value):
        if self.size + 1 > self.capacity:
            raise SymbolTableError("Table is full")
        if key in self.hashtable:
            raise SymbolTableError("Entry: " + key + " already exists")

        self.hashtable[key.upper()] = value
        self.size += 1

    def size(self):
        return self.size

    def dump(self):
        print("Table Dump:")
        for key in self.hashtable:
            print(key, self.hashtable[key])

class SymbolTableEntry:
    def __init__(self):
        self.reserved = False

    def is_variable(self):
        return False
    def is_procedure(self):
        return False
    def is_function(self):
        return False
    def is_functionResult(self):
        return False
    def is_parameter(self):
        return False
    def is_array(self):
        return False
    def is_reserved(self):
        return self.reserved

class ArrayEntry(SymbolTableEntry):
    def __init__(self, name, address, type, upper_bound, lower_bound):
        self.name = name
        self.address = address
        self.type = type
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def is_array(self):
        return True

class ConstantEntry(SymbolTableEntry):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def is_constant(self):
        return True

class FunctionEntry(SymbolTableEntry):
    def __init__(self, name, num_params, param_info, result):
        self.name = name
        self.num_params = num_params
        self.param_info = param_info
        self.result = result

    def is_function(self):
        return True

class ProcedureEntry(SymbolTableEntry):
    def __init__(self, name, num_params, param_info):
        self.name = name
        self.num_params = num_params
        self.param_info =  param_info

    def is_procedure(self):
        return True

class VariableEntry(SymbolTableEntry):
    def __init__(self, name, address, type):
        self.name = name
        self.address = address
        self.type = type

    def is_variable(self):
        return True

class IODeviceEntry(SymbolTableEntry):
    def __init__(self, name):
        self.name = name