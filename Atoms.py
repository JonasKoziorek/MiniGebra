import ast
import numpy as np

from Simplifiers import (DivisionSimplifier, 
                         MultiplicationSimplifier, 
                         PlusSimplifier, 
                         MinusSimplifier,
                         FunctionSimplifier,
                         ExpSimplifier,
                         LnSimplifier,
                         ExponentiationSimplifier,
                         )

from Formatters import (DivisionFormatter,
                            MultiplicationFormatter,
                            PlusFormatter,
                            MinusFormatter,
                            ExponentiationFormatter,
                            FunctionFormatter,
                            )

from Differentiators import (DivisionDifferentiator,
                             MultiplicationDifferentiator,
                             PlusDifferentiator,
                             MinusDifferentiator,
                             ExponentiationDifferentiator,
                             FunctionDifferentiator,
                             SinDifferentiator,
                             CosDifferentiator,
                             TanDifferentiator,
                             ExpDifferentiator,
                             LnDifferentiator
                             )

class Atom:
    def __init__(self):
        pass

    def __add__(self, other):
        return Plus(self, other)
    
    def __sub__(self, other):
        return Minus(self, other)
    
    def __mul__(self, other):
        return Multiplication(self, other)

    def __truediv__(self, other):
        return Division(self, other)

    def __pow__(self, other):
        return Exponentiation(self, other)

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

class Division(BinaryOperator):
    def __repr__(self):
        return DivisionFormatter(self.left, self.right).string_format()

    def diff(self):
        return DivisionDifferentiator(self.left, self.right).diff()

    def simplify(self):
        return DivisionSimplifier(self.left, self.right).simplify()

class Multiplication(BinaryOperator):
    def __repr__(self):
        return MultiplicationFormatter(self.left, self.right).string_format()

    def diff(self):
        return MultiplicationDifferentiator(self.left, self.right).diff()

    def simplify(self):
        return MultiplicationSimplifier(self.left, self.right).simplify()

class Plus(BinaryOperator):
    def __repr__(self):
        return PlusFormatter(self.left, self.right).string_format()

    def diff(self):
        return PlusDifferentiator(self.left, self.right).diff()

    def simplify(self):
        return PlusSimplifier(self.left, self.right).simplify()

class Minus(BinaryOperator):
    def __repr__(self):
        return MinusFormatter(self.left, self.right).string_format()

    def diff(self):
        return MinusDifferentiator(self.left, self.right).diff()

    def simplify(self):
        return MinusSimplifier(self.left, self.right).simplify()

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
        return FunctionSimplifier(self.args, self.name).simplify()

    def __repr__(self):
        return FunctionFormatter(self.name, self.args).string_format()

    def diff(self):
        return FunctionDifferentiator(self.name, self.args).diff()
        

class Sin(Function):
    name = "sin"
    def __init__(self, args):
        super().__init__(self.name, args, np.sin)

    def diff(self):
        return SinDifferentiator(self.name, self.args).diff()

class Cos(Function):
    name = "cos"
    def __init__(self, args):
        super().__init__(self.name, args, np.cos)

    def diff(self):
        return CosDifferentiator(self.name, self.args).diff()

class Tan(Function):
    name = "tan"
    def __init__(self, args):
        super().__init__(self.name, args, np.tan)

    def diff(self):
        return TanDifferentiator(self.name, self.args).diff()

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
        return ExpDifferentiator(self.name, self.args).diff()
    
    def simplify(self):
        return ExpSimplifier(self.args).simplify()

class Ln(Function):
    name = "ln"
    def __init__(self, args):
        super().__init__(self.name, args, np.log)

    def diff(self):
        return LnDifferentiator(self.name, self.args).diff()


    def simplify(self):
        return LnSimplifier(self.args).simplify()

class Exponentiation(BinaryOperator):
    def __repr__(self):
        return ExponentiationFormatter(self.left, self.right).string_format()
    
    def simplify(self):
        return ExponentiationSimplifier(self.left, self.right).simplify()

    def diff(self):
        return ExponentiationDifferentiator(self.left, self.right).diff()

built_in_functions = [Sin, Cos, Tan, Asin, Acos, Atan, Exp, Ln]