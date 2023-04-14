from Tokenizer import tokens, Tokenizer
from Parser import Parser
from Atoms import built_in_functions
from Interpreter import Interpreter
from Preprocessor import Preprocessor
from Errors import *

def compile_input(text):
    try:
        commands, exprs = Preprocessor(text).preprocess()
        t = Tokenizer(tokens)
        p = Parser(t)
        return [p.parse_command(comm) for comm in commands], [p.parse_expr(expr) for expr in exprs]

    except Exception as e:
        print(e)
        return None, None

while True:
    text = input("MiniGebra> ")
    commands, expressions = compile_input(text)
    if commands:
        print("Commands:")
        for command in commands:
            print(command)
        print("")

    if expressions:
        try:
            I = Interpreter(built_in_functions)
            I.feed(expressions)
            print("Expressions:")
            I.print()
            I.simplify_expr()
            print("Simplification:")
            I.print()
            print("Derivatives:")
            I.diff()
            I.simplify_expr()
            I.print()
        except Exception as e:
            print(e)
        print("")