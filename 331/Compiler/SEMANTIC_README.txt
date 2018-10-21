files:
~new~
stack.py
semantic_action.py 
README (THIS FILE)

Bug fixes:
lexer.py:

notes:
- using a list as a stack as always in python tradition (maybe?)

addition:
Lexer Fix
- line 158-159, there should be a digit even after E+ or E- in a numerical constant
- line 168-169, there should not be any alphabetical characters as part of a numerical constant. Only punctuation, space and comment can mark an end of a constant.

Stack Class


TODO:
- backup old parser and modify parser so that it can regconize the augmented grammar
- stack class replace the stack in parser
