CMPU331 - Semantic Action I
David Chenmei
-----------------------

Description
-----------------------
Implementation for semantic actions #1, #2, #3, #4, #6, #7, #9, #13

Files
-----------------------
~ new ~
semantic_action.py 
augmented_grammar.txt
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
symbol_table.py
SYMTAB_README.txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run parser.py (where __main__ is located)
3. (Testing) modify sem_one_test.txt

Issues and Notes
-----------------------
* Assumes one global and local table for now. There might be need for more than one local table or housekeeping inside the local table or even local table within itself later.

* Assumes an arbitrary capacity for global and local table for now.

* Parser was not able to regconize lines of grammar such as 39 because the production number was negative when given. Modified the "non_terminal" method in 
  parser to also check the negative productions if they are not empty (epsilon) which covers these edge cases.

Changelog
-----------------------
* Symbol Table 
- added reserved variable for is_reserved in entry parent class to be overriden during runtime

* Parser 
- Added another else if clause to handle the augmented grammar 
- Added previous token member variable needed for semantic action, meaning anytime "next_token" 
is called, the previous is stored first. 
- Switched from general "Compiler Error" to "Parser Error" overlooked last time

* Grammar (the class) 
- grammar updated to handle actions
- added is_action boolean function, useful for parser 

* Lexer 
- line 158-159, check for a digit even after E+ or E- in a numerical constant
- line 168-169, check for alphabetic characters, which should not end a constant or be part of it

* Error 
- added SemanticActionError 
