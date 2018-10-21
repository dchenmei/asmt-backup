class SemanticAction:
    def __init__(self):
        self.stack = []
        # these are assumed to be private (i.e. don't call them outside of the class!)
        self.insert = True # True = insert mode, False = search mode
        self.global_env = True # True = Global, False = local
        self.is_array = True # True = array, False = simple variable
        self.global_mem = 0
        self.local_mem = 0

    def execute(self, action_num, token):
        stack_top = stack[-1]


    def dump(self):
        print("Stack ::==>", list(reversed(self.stack)))

if __name__ == '__main__':
    print("HELLO WORLD, ONCE AGAIN")
    action = SemanticAction()