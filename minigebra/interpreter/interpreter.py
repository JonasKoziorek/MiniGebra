from PyQt5.QtWidgets import QApplication
import sys

from .atoms import Function, BinaryOperator, Atom
from .tokenizer import tokens, Tokenizer
from .parser import Parser
from .preprocessor import Preprocessor
from .database import Database
from .commands import Command

from ..gui.canvas import Canvas, PlotData

class Interpreter:

    def __init__(self, database: Database = Database()):
        self.database = database
        self.database.expressions = self.database.expressions
        self.functions = self.database.built_in_functions
        self.names = [el.name for el in self.functions]

    def set_build_in_functions(self, functions):
        self.functions = functions

    def feed(self, expressions):
        self.database.expressions = [expressions]
        self.rename_funcs()

    def print_expressions(self, padding=1):
        print("Expressions:")
        pad = "\t" * padding
        expressions = self.database.expressions[0]
        for expr in expressions:
            print(pad+str(expr))

    def print_derivations(self, padding=1):
        derivations = self.database.expressions[1:]
        pad = "\t" * padding
        for rank, diffs in enumerate(derivations):
            print(f"Differentiations of order {rank+1}:")
            for diff in diffs:
                print(pad+str(diff))

    def print(self, padding=1):
        self.print_expressions(padding=padding)
        self.print_derivations(padding=padding)

    def add_func(self, func: tuple[str, Function]):
        self.functions.append(func)
        self.names = self.names.append(func.name)

    def rename_funcs(self):
        self.database.expressions = [[self.rename_func(expr) for expr in elem] for elem in self.database.expressions]

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
        expr = self.database.expressions[0]
        self.database.expressions=[expr]

        for i in range(diff_order):
            expr = [i.diff() for i in expr]
            self.database.expressions.append(expr)


    def simplify(self) -> list:
        self.database.expressions = [[self.__simplify_internal(expr) for expr in elem] for elem in self.database.expressions]

    def generate_data(self):
        self.database.plot_data = [[PlotData(expr, self.database.variables, self.database.domain, self.database.precision) for expr in elem] for elem in self.database.expressions]
        # return [PlotData(expr, self.variables, domain, precision) for elem in self.database.expressions for expr in elem]

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

    def interpret_exprs(self, exprs: list[Atom]):
        self.feed(exprs)
        self.diff(self.database.diff_order)
        self.simplify()

    def interpret_commands(self, commands: list[Command]):
        for command in commands:
            name = command.name
            if name == "vars":
                self.database.variables = command.params
            elif name == "params":
                self.database.parameters = command.params
            elif name == "domain":
                self.database.domain = (command.params[0], command.params[1])
            elif name == "precision":
                self.database.precision = float(command.params[0])
            elif name == "diff_order":
                self.database.diff_order = int(command.params[0])
        
    def interpreter_loop(self, plot=False, padding=1):
        while True:
            text = input("MiniGebra> ")
            commands, expressions = self.compile(text)
            if commands:
                self.print_commands(commands, padding=padding)

            if expressions:
                try:
                    self.interpret_exprs(expressions)
                    self.print(padding=padding)
                    if plot:
                        self.generate_data()
                        app = QApplication(sys.argv)
                        c = Canvas()
                        c.montage(self.database.data)
                        c.show()
                        sys.exit(app.exec_())

                except Exception as e:
                    print(e)
                print("")

    def interpret_text(self, input):
        commands, expressions = self.compile(input)
        self.interpret_exprs(expressions)
        self.interpret_commands(commands)