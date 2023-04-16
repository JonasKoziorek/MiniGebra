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

# while True:
#     text = input("MiniGebra> ")
#     commands, expressions = compile_input(text)
#     if commands:
#         print("Commands:")
#         for command in commands:
#             print(command)
#         print("")

#     if expressions:
#         try:
#             I = Interpreter(built_in_functions)
#             I.feed(expressions)
#             I.diff(1)
#             I.simplify()
#             I.print()
#             I.plot((-10,10))
#         except Exception as e:
#             print(e)
#             pass
#         print("")

def compile_(text):
    commands, expressions = compile_input(text)
    I = Interpreter(built_in_functions)
    I.feed(expressions)
    I.simplify()
    return I.generate_data((-10,10), 0.01)