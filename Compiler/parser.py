from lexer import Lexer
from grammar import Grammar
from error import CompilerError

class Parser:
    def __init__(self, lexer, grammar):
        self.stack = ["ENDOFFILE", "<Goal>"] # note: end is top of the stack
        self.top = self.stack[-1]
        self.lexer = lexer
        self.token = self.lexer.next_token()
        self.grammar = grammar
        self.step = 1

    def dump_stack(self):
        print("Stack ::==>", list(reversed(self.stack)))

    def append_stack(self, unit):
        self.stack.append(unit)
        self.top = self.stack[-1]

    def pop_stack(self):
        self.stack.pop()

        if self.stack:
            self.top = self.stack[-1]

    def next_token(self):
        self.token = self.lexer.next_token()

    def parse(self, debug = 0):
        while self.stack:
            if debug == 1:
                print(">>-  " + str(self.step) + "  -<<")
                self.dump_stack()

            if self.top.upper() == self.token.type():
                self.match(debug)
            elif self.grammar.is_non_term(self.top):
                self.non_terminal(self.token, self.top, debug)
            else:
                self.no_match_error(self.token, self.top, self.token.line())

            if debug == 1:
                self.step += 1
                print()

        print("! ACCEPT !")

    def match(self, debug = 0):
        if debug:
            print("Popped " + self.top.upper() + " with token " + self.token.type() + " -> * MATCH *   {consume tokens}")

        self.pop_stack()
        self.next_token()

    def non_terminal(self, token, top, debug = 0):
        prod_num = self.grammar.prod_num(token.type(), top)

        if prod_num == 999:
            self.production_error(token, top)

        if debug:
            print("Popped", top, "with token", token.type(), end='')

        self.pop_stack()

        # anticipate production, ignore if epsilon
        prod = self.grammar.prod(prod_num)
        if prod_num > 0:
            for unit in reversed(prod):
                if unit is not '': # catches epsilon production that have positive number on the table
                    self.append_stack(unit)

        if debug and prod_num > 0:
            print(" -> $ PUSH $  ", "[", prod_num, "]", top, "::=", prod)
        else:
            print(" -> @ EPSILON @  ", "[", abs(prod_num), "]", top, "::= @ EPSILON @")

    def no_match_error(self, token, top, line):
        if token.value():
            val = token.value().lower()
        else:
            val = ""

        raise CompilerError("Expected " + top.lower() + " before " + token.type().lower() + ": " + val + " on line " + str(line))

    def production_error(self, token, top):
        raise CompilerError("Expected type " + top.lower() + " but provided '" + token.type().lower() +  "' on line " + str(token.line()))

if __name__ == '__main__':
    lexer = Lexer('test_program.txt')
    grammar = Grammar("grammar.txt", "table.txt")
    parser = Parser(lexer, grammar)
    parser.parse(1)