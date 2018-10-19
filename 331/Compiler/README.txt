CMPU331 - Symbol Table
David Chenmei
-----------------------

Description
-----------------------
Class definition for symbol table and its various entry types

Files
-----------------------
~ new ~
symbol_table.py
README.txt (this file)

~ old ~
lexer.py 
token.py
error.py
test.txt
LEXER_README.txt
parser.py
grammar.py
test_program.txt
grammar.txt
table.txt
PARSE_README..txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run symbol_table.py (where __main__ is located)
3. (Testing) modify capacity and add entries in __main__

Issues and Notes
-----------------------
* isFunctionResult, isParameter, and isReserved will be overriden during semantic action
* Implementation uses capacity to limit how big the table can grow, throws error if full
* Table dump prints the raw format of SymbolTableEntry, add a print method in the future

Changelog
-----------------------
* SymbolTableError class added, similar to LexerError and ParserError
