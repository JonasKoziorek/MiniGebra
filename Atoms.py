import ast
import numpy as np

import Simplifiers as Simplifiers
import Formatters as Formatters
import Differentiators as Differentiators

class Atom:
    def __init__(self):
        self.init_args = ()

    def __add__(self, other):
        return self.__work_with_numbers(Plus, other)
    
    def __sub__(self, other):
        return self.__work_with_numbers(Minus, other)
    
    def __mul__(self, other):
        return self.__work_with_numbers(Mul, other)

    def __truediv__(self, other):
        return self.__work_with_numbers(Div, other)

    def __pow__(self, other):
        return self.__work_with_numbers(Expon, other)

    def get_simplifier(self):
        name = self.__class__.__name__
        func = eval(f"Simplifiers.{name}")
        return func(*self.init_args)

    def simplify(self):
        return self.get_simplifier().simplify()

    def simplify_expr(self):
        return self.get_simplifier().simplify_expr()

    def simplify_list(self):
        return self.get_simplifier().simplify_list()

    def get_differentiator(self):
        name = self.__class__.__name__
        func = eval(f"Differentiators.{name}")
        return func(*self.init_args)

    def diff(self):
        return self.get_differentiator().diff()

    def get_formatter(self):
        name = self.__class__.__name__
        func =  eval(f"Formatters.{name}")
        return func(*self.init_args)

    def __repr__(self):
        return self.get_formatter().string_format()

    def to_ast(self, list_):
        return list_[0]

    def to_list(self):
        return [self]

    def eval(dict: dict) -> float:
        pass

    def __call__(self, *args):
        return self.eval(*args)

    def __work_with_numbers(self, operation, other):
        if type(other) == int or type(other) == float:
            return operation(self, Num(other))
        else:
            return operation(self, other)


class BinaryOperator(Atom):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.init_args = (self.left, self.right, self)

    def _to_list(self, operation):
        a=[]; b=[]
        left=self.left; right=self.right

        if type(left) == operation:
            a = left.to_list()
        else:
            a.append(left)
        
        if type(right) == operation:
            b = right.to_list()
        else:
            b.append(right)
        
        return a+b

    def _to_ast(self, list_, operation):
        if len(list_) == 1:
            return list_[0]
        else:
            return operation(list_[0], self._to_ast(list_[1:], operation))

    def to_list(self):
        return self._to_list(type(self))

    def to_ast(self, list_):
        return self._to_ast(list_, type(self))

class Div(BinaryOperator):
    def eval(self, dict: dict):
        return self.left.eval(dict) / self.right.eval(dict)

class Mul(BinaryOperator):
    def eval(self, dict: dict):
        return self.left.eval(dict) * self.right.eval(dict)

class Plus(BinaryOperator):
    def eval(self, dict: dict):
        return self.left.eval(dict) + self.right.eval(dict)

class Minus(BinaryOperator):
    def eval(self, dict: dict):
        return self.left.eval(dict) - self.right.eval(dict)

class Expon(BinaryOperator):
    def eval(self, dict: dict):
        return self.left.eval(dict) ** self.right.eval(dict)

class Num(Atom):
    def __init__(self, value):
        self.value = str(value)
        self.num = self.convert()
        self.init_args = (self.value, self)

    def convert(self):
        return ast.literal_eval(self.value)

    def __eq__(self, other):
        if isinstance(other, Num):
            return self.value == other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.num == other
        else:
            return False

    def __add__(self, other):
        if type(other) == Num:
            return Num(self.num+other.num)
        else:
            return super().__add__(other)
    
    def __sub__(self, other):
        if type(other) == Num:
            return Num(self.num-other.num)
        else:
            return super().__sub__(other)
    
    def __mul__(self, other):
        if type(other) == Num:
            return Num(self.num*other.num)
        else:
            return super().__mul__(other)

    def __pow__(self, other):
        if type(other) == Num:
            return Num(self.num**other.num)
        else:
            return super().__pow__(other)

    def eval(self, dict: dict):
        return self.num

class Var(Atom):
    def __init__(self, value):
        self.value = value
        self.init_args = (self.value, self)

    def eval(self, dict: dict):
        try:
            return dict[self.value]
        except:
            raise Exception(f"Var {self.value} has no specified value.")

class Function(Atom):
    def __init__(self, name, args, func = None):
        self.name = name
        if type(args) != list:
            self.args = [args]
        else:
            self.args = args
        self.func = func
        self.init_args = (self.name, self.args, self)

    def eval(self, dict: dict):
        args = tuple([a.eval(dict) for a in self.args])
        return self.func(*args)

class Sin(Function):
    name = "sin"
    def __init__(self, args):
        super().__init__(self.name, args, np.sin)

class Cos(Function):
    name = "cos"
    def __init__(self, args):
        super().__init__(self.name, args, np.cos)

class Tan(Function):
    name = "tan"
    def __init__(self, args):
        super().__init__(self.name, args, np.tan)

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

class Ln(Function):
    name = "ln"
    def __init__(self, args):
        super().__init__(self.name, args, np.log)

built_in_functions = [Sin, Cos, Tan, Asin, Acos, Atan, Exp, Ln]