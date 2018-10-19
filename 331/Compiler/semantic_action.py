# These are auxiliary classes that make the code more readable, can be refactored later
class AccessMode:
    SEARCH = 0
    INSERT = 1

class Env:
    GLOBAL = 0
    LOCAL = 1

class SemanticAction:
    def __init__(self):
        self.stack = []
        # these are assumed to be private (i.e. don't call them outside of the class!)
        self.acess_mode = AccessMode.INSERT
        self.env = Env.GLOBAL
        self.is_array = 0 # 0 means not array or simple and vice versa
        self.next_global_mem = 0
        self.next_local_mem = 0

    def execute(self, action_num, token):
        print("HI IT'S ME, COMPUTER!")

    def dump(self):
        print("DUMPTY DUMP DUMPING")

if __name__ == '__main__':
    print("HELLO WORLD, ONCE AGAIN")