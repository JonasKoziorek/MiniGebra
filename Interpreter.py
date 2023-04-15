from Atoms import Function, BinaryOperator
import matplotlib.pyplot as plt
import numpy as np

class Interpreter:

    def __init__(self, built_in_functions):
        self.expressions = []
        self.variables = []
        self.parameters = []

        self.functions = built_in_functions
        self.names = [el.name for el in self.functions]

    def feed(self, expressions):
        self.expressions = expressions
        self.rename_funcs()

    def print(self):
        print(self.expressions)

    def fprint(self):
        # full print, prints more information
        print("".join([self.__fprint_expr(expr) for expr in self.expressions]))

    def __fprint_expr(self, expression, increment = 0):
        string = "" 
        if isinstance(expression, BinaryOperator):
            string += "\n" + "\t"*increment + expression.__class__.__name__
            string += self.__fprint_expr(expression.left, increment + 1)
            string += self.__fprint_expr(expression.right, increment + 1)
        else:
            string += "\n" + "\t"*increment + str(expression)

        return string

    def add_func(self, func: tuple[str, Function]):
        self.functions.append(func)
        self.names = self.names.append(func.name)

    def rename_funcs(self):
        self.expressions = [self.rename_func(expr) for expr in self.expressions]

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

    def diff(self) -> list:
        self.expressions = [expr.diff() for expr in self.expressions]

    def simplify(self) -> list:
        self.expressions = [self.__simplify_internal(expr) for expr in self.expressions]

    def eval(self, dict: dict) -> list:
        self.expressions = [expr.eval(dict) for expr in self.expressions]

    def plot(self, interval):
        expr = self.expressions[0]
        a,b = interval
        precision = 1000
        x = np.linspace(a,b,precision)
        y = np.array([expr.eval({"x": i}) for i in x])

        figure, axis = plt.subplots(1, 2)
        
        axis[0].plot(x, y)
        axis[0].set_title("Function")
        
        self.diff()
        expr = self.expressions[0]
        y = np.array([expr.eval({"x": i}) for i in x])
        axis[1].plot(x, y)
        axis[1].set_title("Function derivative")
        
        plt.show()

    def __simplify_internal(self, expr):
        simplified = expr.simplify()
        while str(simplified) != str(expr):
           expr = simplified 
           simplified = expr.simplify()
        return simplified
