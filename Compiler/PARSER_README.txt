CMPU331 - Parser
David Chenmei
-----------------------

Description
-----------------------
Takes in test_program.txt (same directory as parser.py) and prints "! ACCEPT !" if parse is successful.

Files
-----------------------
~ new ~
parser.py
grammar.py
test_program.txt
grammar.txt
table.txt
README.txt (this file)

~ old ~
lexer.py 
token.py
error.py
test.txt
LEXER_README.txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run parser.py (where __main__ is located)
3. (Testing) add program to "test_program.txt" 
4. (Debugging) Parser.parse(debug) default is 0 or off, pass one for step by step output

Issues and Notes
-----------------------
* on grammar implementation:
  with current grammar implementation, one can load "grammar.txt" and "table.txt" and a grammar
  that the parser can use will be generated. It takes advantage of quick access data structure
  that parser will benefit from its frequent requests. For production, dictionary is used to map
  the rule number to the right hand side. For production, two label lists of terminal and non-terminal
  are enumerated. Then the production number table itself is a 2D matrix. To get production number,
  terminal value is used as the row and non-terminal value as column.
  
* error message are generated from parser.py, might be more suitable from error.py
* __main__ is in parser.py for convenience and can easily be relocated
* programs that have quotation marks ("") will return a lexical error

Changelog
-----------------------
* changed following token names to match the grammar:
  LEFTBRACKET  -> LBRACKET
  RIGHTBRACKET -> RBRACKET
  LEFTPAREN    -> LPAREN
  RIGHTPAREN   -> RPAREN

* added line property to tokens:
  they are not printed with the token but is there for error output

* ParserError class added, similar to LexerError


          tidying up the code
		  adding your own test file
