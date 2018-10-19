Bug fixes:
lexer.py:

notes:
- Two classes AccessMode and Env to act as enum so we don't have to guess about what 0 or 1 means in our code!!! This is not necessary with is_array, because it is obvious what it means
- using a list as a stack as always in python tradition

addition:
- line 158-159, there should be a digit even after E+ or E- in a numerical constant
- line 168-169, there should not be any alphabetical characters as part of a numerical constant. Only punctuation, space and comment can mark an end of a constant.
