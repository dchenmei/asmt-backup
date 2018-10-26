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

    def isVariable(self):
        return False
    def isProcedure(self):
        return False
    def isFunction(self):
        return False
    def isFunctionResult(self):
        return False
    def isParameter(self):
        return False
    def isArray(self):
        return False
    def isReserved(self):
        return self.reserved

class ArrayEntry(SymbolTableEntry):
    def __init__(self, name, address, type, upper_bound, lower_bound):
        self.name = name
        self.address = address
        self.type = type
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def isArray(self):
        return True

class ConstantEntry(SymbolTableEntry):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class FunctionEntry(SymbolTableEntry):
    def __init__(self, name, num_params, param_info, result):
        self.name = name
        self.num_params = num_params
        self.param_info = param_info
        self.result = result

    def isFunction(self):
        return True

class ProcedureEntry(SymbolTableEntry):
    def __init__(self, name, num_params, param_info):
        self.name = name
        self.num_params = num_params
        self.param_info =  param_info

    def isProcedure(self):
        return True

class VariableEntry(SymbolTableEntry):
    def __init__(self, name, address, type):
        self.name = name
        self.address = address
        self.type = type

    def isVariable(self):
        return True

class IODeviceEntry(SymbolTableEntry):
    def __init__(self, name):
        self.name = name

'''
if __name__ == '__main__':
    capacity = 6
    table = SymbolTable(capacity)

    # Below examples are imaginary and does not correspond to Vascal and meant for testing the class itself
    table.insert("foo", VariableEntry("foo", 123, "string"))
    table.insert("bar", VariableEntry("bar", 321, "string"))
    table.insert("add", FunctionEntry("add", 2, {"int", "int"}, None))
    table.insert("grades", ArrayEntry("grades", 888, "int", 111, 000))
    table.insert("balance", ConstantEntry("balance", "float"))

    # uncomment following lines to trigger duplicate error and full table error
    #table.insert("foo", ArrayEntry("foo", 100, "int", 444, 333))
    #table.insert("Hello", IODeviceEntry("file"))

    print("Find:")
    print(table.find("foo"))
    print(table.find("grades"))
    print(table.find("underwater basket weaving"))
    print()

    table.dump()
'''
