files:
~new~
stack.py
semantic_action.py 
README (THIS FILE)
parser.py (updated)
augmented_grammar.txt

Bug fixes:
lexer.py:

notes:
- using a list as a stack as always in python tradition (maybe?)
- only created separated functions for action numbers that require complicated routines (i.e. more than one line)
addition:
Lexer Fix
- line 158-159, there should be a digit even after E+ or E- in a numerical constant
- line 168-169, there should not be any alphabetical characters as part of a numerical constant. Only punctuation, space and comment can mark an end of a constant.

Parser Update
- update parser to handle the augmented grammar (additional else if clause)
- added previous token needed for semantic action, meaning anytime next token is about to be called, the previous is stored. This is done easily by just modifying our next token function with an extra line

Grammar Update
- grammar updated to handle the addded "action" type
- added is_action boolean function which assumes that only semantic action labels start with # sign

Error Class:
- added semantic action error

Stack Class


TODO:
- backup old parser [done]
- remember previous token [done]
- modify parser so that it can regconize the augmented grammar [done]
- actions 4 [need to check type]
- actions 7 [check that it is int constant we need]
- actions 13 [check that identifier check works]
- actions 9 [sorta]
- actions 3 [lol]

- should the local symbol table be flushed occassionally?
- fix symbol table class to have reserved boolean (or maybe boolean for all and then override
  the booleans during subclass initialization
- how to pass line number to semantic action error
- using numbers in variable name ideal?
- should we really import everything from symbol table?
- error handling, many major parts that can go wrong
- test.py where major parts are initialized and what not
- should parser notice user of semantic action in debug mode?
- stack class replace the stack in parser

