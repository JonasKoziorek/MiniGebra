from Tokenizer import tokens, Tokenizer
from Parser import Parser
from Atoms import built_in_functions
from Interpreter import Interpreter
from Preprocessor import Preprocessor

def compile_(text):
    try:
        text = Preprocessor().preprocess(text)
        t = Tokenizer(tokens)
        p = Parser(t)
        r = p.read(text)
        return r
    except Exception as e:
        print(e)
        return None

while True:
    text = input("MiniGebra> ")
    r = compile_(text)
    if r:
        I = Interpreter(built_in_functions)
        I.feed([r])
        print("Expression:")
        I.print()
        I.simplify()
        print("Simplification:")
        I.print()
        print("Derivation:")
        I.diff()
        I.simplify()
        I.print()