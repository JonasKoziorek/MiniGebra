from Atoms import Function, BinaryOperator, Atom
import numpy as np
from Tokenizer import tokens, Tokenizer
from Parser import Parser
from Preprocessor import Preprocessor
from Errors import *

from PyQt5.QtWidgets import QApplication
import sys
from Canvas import Canvas, PlotData

class Interpreter:

    def __init__(self, built_in_functions=[]):
        self.expressions = []
        self.variables = ["x"]
        # self.parameters = {}

        self.functions = built_in_functions
        self.names = [el.name for el in self.functions]

    def set_build_in_functions(self, functions):
        self.functions = functions

    def feed(self, expressions):
        self.expressions = [expressions]
        self.rename_funcs()

    def print_expressions(self, padding=1):
        print("Expressions:")
        pad = "\t" * padding
        expressions = self.expressions[0]
        for expr in expressions:
            print(pad+str(expr))

    def print_derivations(self, padding=1):
        derivations = self.expressions[1:]
        pad = "\t" * padding
        for rank, diffs in enumerate(derivations):
            print(f"Differentiations of order {rank+1}:")
            for diff in diffs:
                print(pad+str(diff))

    def print(self, padding=1):
        self.print_expressions(padding=padding)
        self.print_derivations(padding=padding)

    # def fprint(self):
    #     # full print, prints more information
    #     print("".join([self.__fprint_expr(expr) for expr in self.expressions]))

    # def __fprint_expr(self, expression, increment = 0):
    #     string = "" 
    #     if isinstance(expression, BinaryOperator):
    #         string += "\n" + "\t"*increment + expression.__class__.__name__
    #         string += self.__fprint_expr(expression.left, increment + 1)
    #         string += self.__fprint_expr(expression.right, increment + 1)
    #     else:
    #         string += "\n" + "\t"*increment + str(expression)

    #     return string

    def add_func(self, func: tuple[str, Function]):
        self.functions.append(func)
        self.names = self.names.append(func.name)

    def rename_funcs(self):
        self.expressions = [[self.rename_func(expr) for expr in elem] for elem in self.expressions]

    def rename_func(self, expr):
        if isinstance(expr, Function):
            try:
                index = self.names.index(expr.name)
                func =  self.functions[index]
                return func([self.rename_func(i) for i  in expr.args])
            except ValueError:
                return expr

        elif isinstance(expr, BinaryOperator):
            operation = type(expr)
            return operation(self.rename_func(expr.left), self.rename_func(expr.right))

        else:
            return expr

    def diff(self, diff_order = 1) -> list:
        expr = self.expressions[0]
        self.expressions=[expr]

        for i in range(diff_order):
            expr = [i.diff() for i in expr]
            self.expressions.append(expr)


    def simplify(self) -> list:
        self.expressions = [[self.__simplify_internal(expr) for expr in elem] for elem in self.expressions]

    # def eval(self, dict: dict) -> list:
    #     self.expressions = [[expr.eval(dict) for expr in elem] for elem in self.expressions]

    # def generate_data(self, domain: tuple = (-10,10), precision: float = 0.01):
    #     results = []
    #     for elem in self.expressions:
    #         sub_results = []
    #         for expr in elem:
    #             sub_results.append(PlotData(expr, self.variables, domain, precision))
    #         results.append(sub_results)
    #     return results

    def generate_data(self, domain: tuple = (-10,10), precision: float = 0.01):
        return [[PlotData(expr, self.variables, domain, precision) for expr in elem] for elem in self.expressions]

    # def generate_data(self, **kwargs):
    #     return [[self.generate_data_for_expr(expr, **kwargs) for expr in elem] for elem in self.expressions]

    # def generate_data_for_expr(self, expr, interval: tuple = (-10,10), precision: float = 0.01):
    #     a,b = interval
    #     num = int(np.abs(b-a)/precision)
    #     x = np.linspace(a,b,num)
    #     y = np.array([expr.eval({"x": i}) for i in x])
    #     return (x,y)

    def __simplify_internal(self, expr):
        simplified = expr.simplify()
        while str(simplified) != str(expr):
           expr = simplified 
           simplified = expr.simplify()
        return simplified

    def compile(self, input):
        try:
            commands, exprs = Preprocessor(input).preprocess()
            t = Tokenizer(tokens)
            p = Parser(t)
            commands = [p.parse_command(comm) for comm in commands]
            expressions = [p.parse_expr(expr) for expr in exprs]
            return commands, expressions

        except Exception as e:
            print(e)
            return None, None

    def print_commands(self, commands:list, padding=1):
        print("Commands:")
        pad = "\t" * padding
        for command in commands:
            print(pad+str(command))
        print("")

    def interpret_exprs(self, exprs: list[Atom], diff_order=1):
        self.feed(exprs)
        self.diff(diff_order)
        self.simplify()

    def interpreter_loop(self, plot=False, domain=(-10,10), precision=0.1, diff_order=1, padding=1):
        while True:
            text = input("MiniGebra> ")
            commands, expressions = self.compile(text)
            if commands:
                self.print_commands(commands, padding=padding)

            if expressions:
                try:
                    self.interpret_exprs(expressions, diff_order=diff_order)
                    self.print(padding=padding)
                    if plot:
                        data = sum(self.generate_data(domain=domain, precision=precision), [])
                        app = QApplication(sys.argv)
                        c = Canvas()
                        c.montage(data)
                        c.show()
                        sys.exit(app.exec_())

                except Exception as e:
                    print(e)
                print("")

    def interpret_text(self, input, domain=(-10,10),precision=0.01, diff_order=1):
        commands, expressions = self.compile(input)
        self.interpret_exprs(expressions, diff_order=diff_order)
        return self.generate_data(domain, precision)
