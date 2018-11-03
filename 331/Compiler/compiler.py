from lexer import Lexer
from parser import Parser
from grammar import Grammar

lexer = Lexer('phase_2.vas')
grammar = Grammar("augmented_grammar.txt", "table.txt")
parser = Parser(lexer, grammar)
parser.parse(1)
