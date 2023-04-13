from Tokenizer import tokens, Tokenizer
from Parser import Parser
from Atoms import built_in_functions
from Interpreter import Interpreter
from Preprocessor import Preprocessor

def compile_input(text):
    try:
        commands, exprs = Preprocessor(text).preprocess()
        t = Tokenizer(tokens)
        p = Parser(t)
        return commands, [p.parse(expr) for expr in exprs]

    except Exception as e:
        print(e)
        return None, None

while True:
    text = input("MiniGebra> ")
    commands, expressions = compile_input(text)
    if expressions:
        try:
            I = Interpreter(built_in_functions)
            I.feed(expressions)
            print("Expression:")
            I.print()
            I.simplify()
            print("Simplification:")
            I.print()
            print("Derivation:")
            I.diff()
            I.simplify()
            I.print()
        except Exception as e:
            print(e)