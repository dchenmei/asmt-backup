CMPU331 - Lexical Analyser
David Chenmei
-----------------------

Description
-----------------------
Takes in test.txt (same directory as lexer.py) and prints out tokens in form [type, value].

Files
-----------------------
lexer.py 
token.py
error.py
test.txt
README.txt

Usage
-----------------------
1. Open code in PyCharm (Python 3.5 or above, may not be compatible with Python 2.x.x)
2. Run lexer.py (where __main__ is located)
3. Collect output 
4. (Testing) Redirect or copy output to a text file and use a tool like "diff" to compare results

Issues and Notes:
-----------------------
* In this implementation, something like elseand will not throw an error but group it as an
  identifier. This is probably not a big problem as it will lead to syntax error unless 
  that is intended to be an identifier
* 5.3e. in this implemention results in an error
*  __main__ is in lexer.py for convenience, can be easily migrated to an external file
* addop_flag implementation not very clear, it resets whenever something not ], ), identifier or
* constant is returned but it works 

- what happens when you run out of tokens?
