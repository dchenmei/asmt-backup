CMPU331 - Semantic Action II
David Chenmei
-----------------------

Description
-----------------------
Implementation for semantic actions #31, #40, #41, #42, #43, #44, #45, #46, #48, #55, #56

Files
-----------------------
~ new ~
compiler.py (where code is ran)
sem_two.py 
phase_2.vas
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
sem_one.py (renamed)
SEM1_README.txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run compiler.py
3. (Testing) modify phase_2.vas
4. (Testing) tvi is printed after parser output

Issues and Notes
-----------------------
* Helper functions are inside the semantic action because they have states and will not work otherwise. The only exception is the type check method but it is not used outside of semantic action, so it make senses to have it inside as well. 

* Symbol table entries should ideally have member functions. Then the lookup method can take direct token and entries in the future. For now lookup expects strings

* Addresses are printed as positive regardless of whether it is temporary on line 36 and 40

* Errors like undefined variable can be more specific, like telling the user which variable is undefined

* Quad uses None as placeholders for easier printing

* Capacity of tables is still unknown, might not be necessary

* All actions in "execute" should be done through function calls. It will only grow larger and the code within the elif is not as convenient as code inside a function

* Line 157 and 164 is probably not the most elegant way to check if something is an operator

* Not sure if the check the size and content of the stack should be checked popping. Right now, the program assumes nothing funny will happen

* Line 350 assume only MULOPS, a more specific condition is needed

* Dump is not very pretty, it outputs only the raw format of entries and tokens

Changelog
-----------------------
* Added compiler.py to run all the code

* is_div, is_mod and opcode methods added to Token class

* Fixed bug in action 3 on line 216. Accidentally used token type instead of stack top type.

* Changed the symbol table entry member functions to underscore case to avoid confusion 

* Added is_constant to constant entries
