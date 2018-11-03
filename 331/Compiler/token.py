class Token:
    token_map = { "PROGRAM": ["PROGRAM", None],
                  "BEGIN": ["BEGIN", None],
                  "END": ["END", None],
                  "VAR": ["VAR", None],
                  "FUNCTION": ["FUNCTION", None],
                  "PROCEDURE": ["PROCEDURE", None],
                  "RESULT": ["RESULT", None],
                  "INTEGER": ["INTEGER", None],
                  "REAL": ["REAL", None],
                  "ARRAY": ["ARRAY", None],
                  "OF": ["OF", None],
                  "NOT": ["NOT", None],
                  "IF": ["IF", None],
                  "THEN": ["THEN", None],
                  "ELSE": ["ELSE", None],
                  "WHILE": ["WHILE", None],
                  "DO" : ["DO", None],
                  "*" : ["MULOP", 1],
                  "/" : ["MULOP", 2],
                  "DIV" : ["MULOP", 3],
                  "MOD" : ["MULOP", 4],
                  "AND" : ["MULOP", 5],
                  "+"  : ["ADDOP", 1],
                  "-"  : ["ADDOP", 2],
                  "OR"  : ["ADDOP", 3],
                  "="   : ["RELOP", 1],
                  "<>"   : ["RELOP", 2],
                  "<"   : ["RELOP", 3],
                  ">"   : ["RELOP", 4],
                  "<="   : ["RELOP", 5],
                  ">="   : ["RELOP", 6],
                  ";"   : ["SEMICOLON", None],
                  ","   : ["COMMA", None],
                  "["   : ["LBRACKET", None],
                  "]"   : ["RBRACKET", None],
                  "("   : ["LPAREN", None],
                  ")"   : ["RPAREN", None],
                  ".."  : ["DOUBLEDOT", None],
                  "."   : ["ENDMARKER", None],
                  ":"   : ["COLON", None],
                  ":="  : ["ASSIGNOP", None],
                  "++"  : ["UNARYPLUS", None],
                  "--"  : ["UNARYMINUS", None]
                }

    def __init__(self, type, value, line, map=0):
        if not map:
            self.token = [type, value]
        elif type in self.token_map.keys():
            self.token = self.token_map[type]
        else:
            self.token = ["IDENTIFIER", type]

        self.line_number = line

    def type(self):
        return self.token[0]

    def value(self):
        return self.token[1]

    def line(self):
        return self.line_number

    def op_code(self):
        # DIV and MOD are handled outside of this
        # current only support arithmetic operations
        if self.type() == "MULOP":
            if self.value() == 1:
                return "mul"
            elif self.value() == 2:
                return "div"
        elif self.type() == "ADDOP":
            if self.value() == 1:
                return "add"
            elif self.value() == 2:
                return "sub"
        else:
            print("HELLO")
            raise LookupError

    def is_div(self):
        return self.type() == "MULOP" and self.value() == 3

    def is_mod(self):
        return self.type() == "MULOP" and self.value() == 4

    def str(self):
        str_tk = "['" + self.type() + "', "
        if self.value() is None:
            str_tk += "None]"
        elif type(self.value()) is int:
            str_tk += str(self.value()) + "]"
        else:
            str_tk += "'" + self.value() + "']"

        return str_tk