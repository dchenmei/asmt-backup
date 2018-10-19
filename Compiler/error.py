import sys

# Custom handler, hides unecessary details
def compiler_handler(type, value, traceback):
    print(value)

sys.excepthook = compiler_handler

class CompilerError(Exception):
    pass

class LexerError(CompilerError):
    def __init__(self, message, line, character):
        super().__init__("Lexical Error: " + message + " at line " + str(line) + ", character " + str(character))

class ParserError(CompilerError):
    def __init__(self, message, line, character):
        super().__init__("Parser Error: " + message + " at line " + str(line) + ", character " + str(character))

class SymbolTableError(CompilerError):
    def __init__(self, message):
        super().__init__("Symbol Table Error: " + message)
