from token import Token
from error import LexerError

def is_punct(c):
    return c in { "=", "<", ">", "*", "/", "+", "-", ",", ":", ";", ".", "[", "]", "(", ")", "+", "-" }

class Lexer:
    def __init__(self, file):
        self.pos = 0
        self.line = 1
        self.char_pos = 0
        self.addop_flag = False
        self.max_id_len = 32

        try:
            self.file = open(file, 'r')
        except FileNotFoundError:
            print("Bad file or path")

        self.buff = (self.file.read()).upper()
        self.end = len(self.buff)

    def next_line(self):
        self.line += 1
        self.char_pos = 0

    def curr_char(self):
        if self.pos < self.end:
            return self.buff[self.pos]
        else:
            return None

    def next_char(self):
        if self.pos + 1 < self.end:
            return self.buff[self.pos + 1]
        else:
            return None

    def forward(self):
        self.pos += 1
        self.char_pos += 1

    def next_token(self):
        if self.pos > self.end:
            return None
        elif self.pos == self.end:
            self.forward()
            return Token("ENDOFFILE", None, self.line)

        curr_char = self.curr_char()
        if curr_char == " " or curr_char == '\t' or curr_char == '\n':
            self.space()
            return self.next_token()
        elif curr_char == '{' or curr_char == '}':
            self.comment()
            return self.next_token()
        elif is_punct(curr_char):
            return self.punct()
        elif curr_char.isalpha():
            return self.letters()
        elif curr_char.isdigit():
            return self.digits()
        else:
            raise LexerError("Invalid character", self.line, self.char_pos)

    def comment(self):
        curr_char = self.curr_char()

        if curr_char == '}':
            raise LexerError("Invalid Comment", self.line, self.char_pos)

        while curr_char and curr_char != '}':
            if curr_char == '\n':
                self.next_line()

            self.forward()
            curr_char = self.curr_char()

        # Unclosed Comment
        if self.pos >= self.end:
            raise LexerError("Invalid Comment", self.line, self.char_pos)

        # Exit Comment
        self.forward()

    def space(self):
        curr_char = self.curr_char()
        while curr_char and (curr_char == ' ' or curr_char == '\n' or curr_char == '\t'):
            if curr_char == '\n':
                self.next_line()

            self.forward()
            curr_char = self.curr_char()

    def letters(self):
        id = ""
        curr_char = self.curr_char()
        while curr_char and (curr_char.isalpha() or curr_char.isdigit()):
            id += curr_char
            self.forward()
            curr_char = self.curr_char()

        if len(id) > self.max_id_len:
            raise LexerError("Identifier too long", self.line, self.char_pos)

        tk = Token(id, None, self.line, 1)
        if tk.type() == "IDENTIFIER":
            self.addop_flag = True
        else:
            self.addop_flag = False # consumed, only valid after one token

        return tk

    def digits(self):
        beg = self.pos # beginning of constant
        curr_char = self.curr_char()
        while curr_char and curr_char.isdigit():
            self.forward()
            curr_char = self.curr_char()

        next_next = self.next_char() # ensures there are more characters after current
        if curr_char == 'E' and next_next:
            return self.big_e(beg)
        elif curr_char == '.' and next_next and next_next != '.':
            return self.decimal(beg)
        elif curr_char.isalpha(): # not including E
            raise LexerError("Invalid constant", self.line, self.char_pos)
        else:
            self.addop_flag = True
            return Token("INTCONSTANT", self.buff[beg : self.pos], self.line)

    def decimal(self, beg):
        self.forward() # skip '.'
        curr_char = self.curr_char()

        # A digit must follow the dot
        if not curr_char or not curr_char.isdigit():
            raise LexerError("Invalid constant", self.line, self.char_pos)

        while curr_char and curr_char.isdigit():
            self.forward()
            curr_char = self.curr_char()

        next_next = self.next_char()
        if curr_char == 'E' and next_next:
            return self.big_e(beg)
        elif curr_char.isalpha():
            raise LexerError("Invalid constant", self.line, self.char_pos)
        else:
            self.addop_flag = True
            return Token("REALCONSTANT", self.buff[beg : self.pos], self.line)

    def big_e(self, beg):
        self.forward() # skip 'E'
        curr_char = self.curr_char()
        if not (curr_char == '+' or curr_char == '-' or curr_char.isdigit()):
            raise LexerError("Invalid constant", self.line, self.char_pos)
        if (curr_char == '+' or curr_char == '-') and not self.next_char().isdigit():
            raise LexerError("Invalid constant", self.line, self.char_pos + 1);

        self.forward() # skip preliminary +, - or digit
        curr_char = self.curr_char()
        while curr_char and curr_char.isdigit():
            self.forward()
            curr_char = self.curr_char()

        # Alphabetical characters are not allowed as part of a number
        if curr_char.isalpha():
            raise LexerError("Invalid constant", self.line, self.char_pos)

        self.addop_flag = True
        return Token("REALCONSTANT", self.buff[beg : self.pos], self.line)

    def punct(self):
        curr_char = self.curr_char()
        self.forward()

        # Try greedily tagging a second character and if no match then discard it
        next_next = self.curr_char()
        if next_next:
            next_next = curr_char + next_next

        tk = Token(next_next, None, self.line, 1)
        if tk.type() == "IDENTIFIER" or curr_char == '+' or curr_char == '-': # also prevents - -- and + ++ mixup
            tk = Token(curr_char, None, self.line, 1)
        else:
            self.forward() # adjust for extra character

        # Addop situations
        if not self.addop_flag and (curr_char == '+' or curr_char == '-'):
            tk = Token(curr_char * 2, None, self.line, 1)
        elif curr_char == ')' or curr_char == ']':
            self.addop_flag = True
        else: #flag is consumed, whether addop or not because it won't be valid after one token return
            self.addop_flag = False

        return tk

if __name__ == '__main__':
    lexer = Lexer('test.txt')
    tk = lexer.next_token()
    while tk is not None:
        print(tk.str())
        tk = lexer.next_token()
