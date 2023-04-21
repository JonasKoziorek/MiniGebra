from PyQt5.QtWidgets import QApplication
import sys

from .atoms import Function, BinaryOperator, Atom
from .tokenizer import Tokenizer
from .parser import Parser
from .preprocessor import Preprocessor
from .database import Database
from .commands import Command

from ..gui.canvas import Canvas, PlotData

class Interpreter:
    """
    This class represents interpreter which accepts parsed math expressions and does operations on them.
    Simplifications, differentiations, evaluations and string representations of parsed expressions are also supported by this class.
    """

    def __init__(self):
        self.database = Database()
        self.database.expressions = self.database.expressions
        self.functions = self.database.built_in_functions
        self.names = [el.name for el in self.functions]

    def set_build_in_functions(self, functions: list[Function]) -> None:
        """
        Specifies built in function that interpreter recognizes.
        """
        self.functions = functions

    def feed(self, expressions: list[Atom]) -> None:
        """
        Accepts parsed math expressions. Locates built-in functions in the parsed expressions.
        """
        self.database.expressions = [expressions]
        self.rename_funcs()

    def print_expressions(self, padding: int = 1) -> None:
        """
        Prints currently held expressions to standard output.
        """
        print("Expressions:")
        pad = "\t" * padding
        expressions = self.database.expressions[0]
        for expr in expressions:
            print(pad+str(expr))

    def print_derivations(self, padding: int = 1) -> None:
        """
        Prints derivatives of currently held expressions to standard output.
        """
        derivations = self.database.expressions[1:]
        pad = "\t" * padding
        for rank, diffs in enumerate(derivations):
            print(f"Differentiations of order {rank+1}:")
            for diff in diffs:
                print(pad+str(diff))

    def print(self, padding=1) -> None:
        """
        Prints expressions and theirs derivatives to standard output.
        """
        self.print_expressions(padding=padding)
        self.print_derivations(padding=padding)

    def rename_funcs(self) -> None:
        """
        Renames functions in inputed parsed expression from general functions to their specific forms. 
        """
        self.database.expressions = [[self.rename_func(expr) for expr in elem] for elem in self.database.expressions]

    def rename_func(self, expr: Atom):
        """
        Checks whether an expr is a built-in function. If so, it converts expr to that function.
        """
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

    def diff(self, diff_order: int = 1) -> None:
        """
        Produces derivatives of the original expressions (up to differentiation order, including).
        """
        expr = self.database.expressions[0]
        self.database.expressions=[expr]

        for i in range(diff_order):
            expr = [i.diff() for i in expr]
            self.database.expressions.append(expr)


    def simplify(self) -> None:
        """
        Simplifies the original expressions.
        """
        self.database.expressions = [[self.__simplify_internal(expr) for expr in elem] for elem in self.database.expressions]

    def generate_data(self) -> None:
        """
        Generates plotting data for each expression and it's derivatives.
        """
        self.database.plot_data = [[PlotData(expr, self.database.variables, self.database.domain, self.database.precision) for expr in elem] for elem in self.database.expressions]

    def __simplify_internal(self, expr: Atom):
        """
        Keeps simplifying the expression recursively until no changes are made.
        """
        simplified = expr.simplify()
        while str(simplified) != str(expr):
           expr = simplified 
           simplified = expr.simplify()
        return simplified

    def compile(self, input):
        """
        Accepts input expressions and commands as strings and produces according commands and expressions from them.
        """
        try:
            commands, exprs = Preprocessor(input).preprocess()
            t = Tokenizer()
            p = Parser(t)
            commands = [p.parse_command(comm) for comm in commands]
            expressions = [p.parse_expr(expr) for expr in exprs]
            return commands, expressions

        except Exception as e:
            print(e)
            return None, None

    def print_commands(self, commands:list, padding: int = 1) -> None:
        """
        Print information about commands on the standart input.
        """
        print("Commands:")
        pad = "\t" * padding
        for command in commands:
            print(pad+str(command))
        print("")

    def interpret_exprs(self, exprs: list[Atom]) -> None:
        """
        Accepts list of expressions as input. Simplifies and differentiates this input. Saves it into the database.
        """
        self.feed(exprs)
        self.diff(self.database.diff_order)
        self.simplify()

    def interpret_commands(self, commands: list[Command]):
        """
        Interprets list of commands and saves information about them into the database.
        """
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
        
    def interpreter_loop(self, plot: bool =False, padding: int =1) -> None:
        """
        Interprets list of commands and saves information about them into the database.
        """
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

    def interpret_text(self, input) -> None:
        commands, expressions = self.compile(input)
        self.interpret_exprs(expressions)
        self.interpret_commands(commands)