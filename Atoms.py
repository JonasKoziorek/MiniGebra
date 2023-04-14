import ast
import numpy as np

# from Simplifiers import (DivSimplifier,
#                          MulSimplifier, 
#                          PlusSimplifier, 
#                          MinusSimplifier,
#                          FunctionSimplifier,
#                          ExpSimplifier,
#                          LnSimplifier,
#                          ExponSimplifier,
#                          )

# from Formatters import (DivFormatter,
#                             MulFormatter,
#                             PlusFormatter,
#                             MinusFormatter,
#                             ExponFormatter,
#                             FunctionFormatter,
#                             )

# from Differentiators import (DivDifferentiator,
#                              MulDifferentiator,
#                              PlusDifferentiator,
#                              MinusDifferentiator,
#                              ExponDifferentiator,
#                              FunctionDifferentiator,
#                              SinDifferentiator,
#                              CosDifferentiator,
#                              TanDifferentiator,
#                              ExpDifferentiator,
#                              LnDifferentiator
#                              )

import Simplifiers as Simplifiers
import Formatters as Formatters
import Differentiators as Differentiators


class Atom:
    def __init__(self):
        pass

    def __add__(self, other):
        return Plus(self, other)
    
    def __sub__(self, other):
        return Minus(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __pow__(self, other):
        return Expon(self, other)

    def simplify(self):
        return self

    def diff(self):
        return self

class BinaryOperator(Atom):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def diff(self):
        return self

    def __repr__(self):
        return f"operator({self.left},{self.right})"

class Div(BinaryOperator):
    def __repr__(self):
        return Formatters.Div(self.left, self.right, self).string_format()

    def diff(self):
        return Differentiators.Div(self.left, self.right, self).diff()

    def simplify(self):
        return Simplifiers.Div(self.left, self.right, self).simplify()

class Mul(BinaryOperator):
    def __repr__(self):
        return Formatters.Mul(self.left, self.right, self).string_format()

    def diff(self):
        return Differentiators.Mul(self.left, self.right, self).diff()

    def simplify(self):
        return Simplifiers.Mul(self.left, self.right, self).simplify()

class Plus(BinaryOperator):
    def __repr__(self):
        return Formatters.Plus(self.left, self.right, self).string_format()

    def diff(self):
        return Differentiators.Plus(self.left, self.right, self).diff()

    def simplify(self):
        return Simplifiers.Plus(self.left, self.right, self).simplify()

class Minus(BinaryOperator):
    def __repr__(self):
        return Formatters.Minus(self.left, self.right, self).string_format()

    def diff(self):
        return Differentiators.Minus(self.left, self.right, self).diff()

    def simplify(self):
        return Simplifiers.Minus(self.left, self.right, self).simplify()

class Number(Atom):
    def __init__(self, value):
        self.value = str(value)
        self.num = self.convert()

    def convert(self):
        return ast.literal_eval(self.value)

    def diff(self):
        return Number(0)

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.num == other
        else:
            return False

class Variable(Atom):
    def __init__(self, value):
        self.value = value

    def diff(self):
        return Number(1)

    def __repr__(self):
        return f"{self.value}"


class Function(Atom):
    def __init__(self, name, args, func = None):
        self.name = name
        if type(args) != list:
            self.args = [args]
        else:
            self.args = args
        self.func = func

    def simplify(self):
        return Simplifiers.Function(self.name, self.args, self).simplify()

    def __repr__(self):
        return Formatters.Function(self.name, self.args, self).string_format()

    def diff(self):
        return Differentiators.Function(self.name, self.args, self).diff()
        

class Sin(Function):
    name = "sin"
    def __init__(self, args):
        super().__init__(self.name, args, np.sin)

    def diff(self):
        return Differentiators.Sin(self.name, self.args, self).diff()

class Cos(Function):
    name = "cos"
    def __init__(self, args):
        super().__init__(self.name, args, np.cos)

    def diff(self):
        return Differentiators.Cos(self.name, self.args, self).diff()

class Tan(Function):
    name = "tan"
    def __init__(self, args):
        super().__init__(self.name, args, np.tan)

    def diff(self):
        return Differentiators.Tan(self.name, self.args, self).diff()

class Asin(Function):
    name = "asin"
    def __init__(self, args):
        super().__init__(self.name, args, np.arcsin)

class Acos(Function):
    name = "acos"
    def __init__(self, args):
        super().__init__(self.name, args, np.arccos)

class Atan(Function):
    name = "atan"
    def __init__(self, args):
        super().__init__(self.name, args, np.arctan)

class Exp(Function):
    name = "exp"
    def __init__(self, args):
        super().__init__(self.name, args, np.exp)

    def diff(self):
        return Differentiators.Exp(self.name, self.args, self).diff()
    
    def simplify(self):
        return Simplifiers.Exp(self.name, self.args, self).simplify()

class Ln(Function):
    name = "ln"
    def __init__(self, args):
        super().__init__(self.name, args, np.log)

    def diff(self):
        return Differentiators.Ln(self.name, self.args, self).diff()


    def simplify(self):
        return Simplifiers.Ln(self.name, self.args, self).simplify()

class Expon(BinaryOperator):
    def __repr__(self):
        return Formatters.Expon(self.left, self.right, self).string_format()
    
    def simplify(self):
        return Simplifiers.Expon(self.left, self.right, self).simplify()

    def diff(self):
        return Differentiators.Expon(self.left, self.right, self).diff()

built_in_functions = [Sin, Cos, Tan, Asin, Acos, Atan, Exp, Ln]