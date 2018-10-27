CMPU331 - Semantic Action II
David Chenmei
-----------------------

Description
-----------------------
Implementation for semantic actions #31, #40, #41, #42, #43, #44, #45, #46, #48, #55, #56

Files
-----------------------
~ new ~
semantic_action.py (updated)
quadruples.py
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
augmented_grammar.txt
SEM1_README.txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run parser.py (where __main__ is located)
3. (Testing) modify sem_two_test.txt

Issues and Notes
-----------------------
* No actual quadruple class is created, as there is no need. A list of string is assumed to be a quadruple, each storing up to four things
* Some things are different than the example of Quadruples in Java. Instead of using a vector, a normal list will suffice and does the same thing. Also for the print, the a string is built first which is a little less complicated.
* Counting from 1 is a little uneasy for quadruple

Changelog
-----------------------

TODO:
Class: Quadruple [ok]
Class: Quadruples [ok]
Function: Typecheck() [ok]
Function: Create()
Function: GetTempVar()
Function: Gen()
Insert reserved words (main, something with in and out)
Update 3 [local memory already handled]
Update 9
Function Backpatch
Variable: GlobalStore and LocalStore
New Routines
