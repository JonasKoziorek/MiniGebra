import ast
import numpy as np
from AtomSimplifiers import (DivisionSimplifier, 
                         MultiplicationSimplifier, 
                         PlusSimplifier, 
                         MinusSimplifier,
                         FunctionSimplifier,
                         ExpSimplifier,
                         LnSimplifier,
                         ExponentiationSimplifier,
                         )

from AtomFormatters import (DivisionFormatter,
                            MultiplicationFormatter,
                            PlusFormatter,
                            MinusFormatter,
                            ExponentiationFormatter,
                            FunctionFormatter,
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
        pass

    def __repr__(self):
        return f"operator({self.left},{self.right})"

class Division(BinaryOperator):
    def __repr__(self):
        left = self.left ; right = self.right
        bracket_types = [Plus, Minus, Division, Exponentiation]
        if type(left) in bracket_types:
            left = f"({self.left})"

        if type(right) in bracket_types:
            right = f"({self.right})"

        return f"{left} / {right}"

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Number(2))

    def simplify(self):
        return DivisionSimplifier(self.left, self.right).simplify()

class Multiplication(BinaryOperator):
    def __repr__(self):
        left = self.left ; right = self.right
        bracket_types = [Plus, Minus, Exponentiation, Division]
        neglect_types = [Number, Function, Variable]
        if type(left) in neglect_types and type(right) == Variable:
            return f"{self.left}{self.right}"

        if type(left) == Number and type(right) == Number:
            return f"{left} * {right}"

        if type(left) in bracket_types:
            left = f"({left})"

        if type(right) in bracket_types:
            right = f"({right})"

        return f"{left}{right}"

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

    def simplify(self):
        return MultiplicationSimplifier(self.left, self.right).simplify()

class Plus(BinaryOperator):
    def __repr__(self):
        return f"{self.left} + {self.right}"

    def diff(self):
        return self.left.diff() + self.right.diff()

    def simplify(self):
        return PlusSimplifier(self.left, self.right).simplify()

class Minus(BinaryOperator):
    def __repr__(self):
        return f"{self.left} - {self.right}"

    def diff(self):
        return self.left.diff() - self.right.diff()

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
    def __init__(self, name, args):
        self.name = name
        if type(args) != list:
            self.args = [args]
        else:
            self.args = args
        self.func = None

    def simplify(self):
        return FunctionSimplifier(self.args, self.name).simplify()

    def __repr__(self):
        return FunctionFormatter(self.name, self.args).string_format()
    
    def _error_message(self):
        raise Exception(f"Function {self.name} only supports single variable differentiating.")

    def diff(self):
        if len(self.args) == 1:
            return self * self.args[0].diff()
        else:
            self._error_message()

class Sin(Function):
    name = "sin"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.sin

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Cos([arg]) * arg.diff()
        else:
            self._error_message()

class Cos(Function):
    name = "cos"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.cos

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Number(-1) * Sin([arg]) * arg.diff()
        else:
            self._error_message()

class Tan(Function):
    name = "tan"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.tan

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Number(1) / (Cos(self.args)*Cos(self.args)) * arg.diff()
        else:
            self._error_message()

class Asin(Function):
    name = "asin"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.arcsin

class Acos(Function):
    name = "acos"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.arccos

class Atan(Function):
    name = "atan"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.arctan

class Exp(Function):
    name = "exp"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.exp

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Exp(arg) * arg.diff()
        else:
            self._error_message()
    
    def simplify(self):
        return ExpSimplifier(self.args).simplify()

class Ln(Function):
    name = "ln"
    def __init__(self, args):
        super().__init__(self.name, args)
        self.func = np.log

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Number(1) / arg * arg.diff()
        else:
            self._error_message()

    def simplify(self):
        return LnSimplifier(self.args).simplify()

class Exponentiation(BinaryOperator):
    def __repr__(self):
        return ExponentiationFormatter(self.left, self.right).string_format()
    
    def simplify(self):
        return ExponentiationSimplifier(self.left, self.right).simplify()

    def diff(self):
        return Exp([self.right * Ln([self.left])]).diff()

built_in_functions = [Sin, Cos, Tan, Asin, Acos, Atan, Exp, Ln]