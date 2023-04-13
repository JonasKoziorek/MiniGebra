import ast
import numpy as np

# sin^2 + cos^2 = 1
# sin/cos = tan
# cos/sin = 1/tan
# expr ^ -a = 1 / (expr ^ a)
# 1 / (expr ^ -a) = (expr ^ a)

# ln a^b = b * ln a
# ln a - ln b = ln (a/b)
# ln a + ln b = ln (a*b)
# a * (b * x) = (a*b)*x
# a ^ b = a^b
# ((x ^ a) ^ b) ^ c = x ^ (a*b*c)
# expr ^ a * expr ^ b = expr ^ (a+b)
# expr ^ 0 = 1
# expr ^ 1 = expr
# reduce fraction
# a/b * c/d = (a*c)/(b*d)
# a*var + b*var = (a+b) * var
# 0 / expr = 0
# expr / 1 = expr
# const / const = const/const
# const * const = const*const
# expr * constant = constant * expr
# expr * 1 = expr
# 1 * expr = expr
# expr * 0 = 0
# 0 * expr = 0
# const + const = const+const
# expr + 0 = expr
# 0 + expr = expr
# const - const = const-const
# expr - 0 = expr
# 0 - expr = expr
# func(expr) = func(expr.simplify())

class Command:
    # known directives:
    # domain: R->R or R->R^2 or R->R^3 or R^2->R or R^2->R^3
    # vars: comma separated words/letters => x, y, az
    # param: comma separated words/letters => a, b, abd
    def __init__(self, text: str):
        self.text = text

    def simplify(self):
        return self

    def diff(self):
        return self

    def __repr__(self):
        return self.text

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
        if type(left) == Plus or type(left) == Minus:
            return f"({self.left}) / {self.right}"

        elif type(right) == Plus or type(right) == Minus:
            return f"{self.left} / ({self.right})"

        else:
            return f"{self.left} / {self.right}"

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Number(2))

    def simplify(self):
        left = self.left
        right = self.right
        # 0 / expr = 0
        if left == 0:
            return Number(0)

        # expr / 1 = expr
        elif right == 1:
            return left.simplify()

        # # const / const = const/const
        # elif type(left) == Number and type(right) == Number:
        #     return Number(left.num / right.num)

        # reduce fraction
        elif type(left) == Number and type(right) == Number:
            a = left.num
            b = right.num
            if type(a) == int and type(b) == int:
                div = np.gcd(a,b)
                a = Number(int(a/div))
                b = Number(int(b/div))
                return Division(a,b)

        else:
            return Division(left.simplify(), right.simplify())

class Multiplication(BinaryOperator):
    def __repr__(self):
        left = self.left ; right = self.right
        if type(left) == Plus or type(left) == Minus:
            return f"({self.left}) / {self.right}"

        elif type(right) == Plus or type(right) == Minus:
            return f"{self.left} / ({self.right})"

        else:
            return f"{self.left} / {self.right}"

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

    def simplify(self):
        left = self.left
        right = self.right
        # 0 * expr = 0
        if left == 0:
            return Number(0)

        # expr * 0 = 0
        elif right == 0:
            return Number(0)

        # 1 * expr = expr
        elif left == 1:
            return right.simplify()

        # expr * 1 = expr
        elif right == 1:
            return left.simplify()

        # expr * constant = constant * expr
        elif type(right) == Number and type(left) != Number:
            return right * left.simplify()

        # const * const = const*const
        elif type(left) == Number and type(right) == Number:
            return Number(left.num * right.num)

        # a/b * c/d = (a*c)/(b*d)
        elif type(left) == Division and type(right) == Division:
            return Division(left.left.simplify() * right.left.simplify(), left.right.simplify() * right.right.simplify())

        # expr ^ a * expr ^ b = expr ^ (a+b)
        elif type(left) == Exponentiation and type(right) == Exponentiation:
            if type(left.right) == Number and type(right.right) == Number and str(left.left) == str(right.left):
                return Exponentiation(left.left.simplify(), left.right.num * right.right.num)
            else:
                return self

        # a * (b * x) = (a*b)*x
        elif type(left) == Number and type(right) == Multiplication and type(right.left) == Number:
            return Multiplication(Number(left.num * right.left.num), right.right.simplify())

        else:
            return Multiplication(left.simplify(), right.simplify())


class Plus(BinaryOperator):
    def __repr__(self):
        return f"{self.left} + {self.right}"

    def diff(self):
        return self.left.diff() + self.right.diff()

    def simplify(self):
        left = self.left
        right = self.right
        # 0 + expr = expr
        if left == 0:
            return right.simplify()
        # expr + 0 = expr
        elif right == 0:
            return left.simplify()
        # const + const = const+const
        elif type(left) == Number and type(right) == Number:
            return Number(left.num + right.num)

        # var + var = (2) * var
        elif type(left) == Variable and type(right) == Variable and left.value == right.value:
                return Number(2) * right

        # a*var + b*var = (a+b) * var
        elif type(left) == Multiplication and type(right) == Multiplication:
            if type(left.left) == Number and type(right.left) == Number and str(left.right) == str(right.right):
                return Number(left.left + left.right) * left.right.simplify()
            else:
                return Plus(left.simplify(), right.simplify())

        # ln a + ln b = ln (a*b)
        elif type(left) == Ln and type(right) == Ln and len(left.args) == 1 and len(right.args) == 1:
            return Ln(left.args[0].simplify() * right.args[0].simplify())

        else:
            return Plus(left.simplify(), right.simplify())

class Minus(BinaryOperator):
    def __repr__(self):
        return f"{self.left} - {self.right}"

    def diff(self):
        return self.left.diff() - self.right.diff()

    def simplify(self):
        left = self.left
        right = self.right
        # 0 - expr = expr
        if left == 0:
            return Number(-1) * right.simplify()

        # expr - 0 = expr
        elif right == 0:
            return left.simplify()

        # const - const = const-const
        elif type(left) == Number and type(right) == Number:
            return Number(left.num + right.num)

        # ln a - ln b = ln (a/b)
        elif type(left) == Ln and type(right) == Ln and len(left.args) == 1 and len(right.args) == 1:
            return Ln(left.args[0].simplify() / right.args[0].simplify())

        # var - var = 0
        elif type(left) == Variable and type(right) == Variable and left.value == right.value:
                return Number(0)

        # a*var - b*var = (a-b) * var
        elif type(left) == Multiplication and type(right) == Multiplication:
            if type(left.left) == Number and type(right.left) == Number and str(left.right) == str(right.right):
                return (left.left - left.right) * left.right.simplify()
            else:
                return Minus(left.simplify(), right.simplify())

        else:
            return Minus(left.simplify(), right.simplify())

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

    # def __add__(self, other):
    #     if isinstance(other, Number):
    #         return Number(self.num + other.num)
    #     else:
    #         return Plus(self, other)
    
    # def __sub__(self, other):
    #     if isinstance(other, Number):
    #         return Number(self.num - other.num)
    #     else:
    #         return Minus(self, other)
    
    # def __mul__(self, other):
    #     if isinstance(other, Number):
    #         return Number(self.num * other.num)
    #     else:
    #         return Multiplication(self, other)

    # def __truediv__(self, other):
    #     if isinstance(other, Number):
    #         return Number(self.num / other.num)
    #     else:
    #         return Division(self, other)


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
        # func(expr) = func(expr.simplify())
        class_ = type(self)
        if class_ in built_in_functions:
            return class_([a.simplify() for a in self.args])
        else:
            return class_(self.name, [a.simplify() for a in self.args])

    def __repr__(self):
        string = str(self.args[0])
        for arg in self.args[1:]:
            string += ", " + str(arg)
        return f"{self.name}({string})"
    
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
        args = self.args
        # ln a^b = b * ln a
        if len(args) == 1 and type(args[0]) == Exponentiation:
            return args[0].right.simplify() * Ln([args[0].left.simplify()])
        else:
            return self

class Exponentiation(BinaryOperator):
    def __repr__(self):
        left = str(self.left)
        right = str(self.right)
        if isinstance(self.right, BinaryOperator):
            right = f"({self.right})"

        if isinstance(self.left, BinaryOperator):
            left = f"({self.left})"

        return f"{left} ^ {right}"
    
    def simplify(self):
        left = self.left
        right = self.right

        # expr ^ 1 = expr
        if type(right) == Number and right == 1:
            return left.simplify()

        # expr ^ 0 = 1
        elif type(right) == Number and right == 0:
            return Number(1)

        # ((x ^ a) ^ b) = x ^ (a*b)
        elif type(left) == Exponentiation and type(right) == Number:
            if type(left.right) == Number:
                return Exponentiation(left.left.simplify(), left.right * right)
            else:
                return self

        # a ^ b = a^b
        elif type(left) == Number and type(right) == Number:
            return Number(left.num ** right.num)
        
        else:
            return self

    def diff(self):
        return Exp([self.right * Ln([self.left])]).diff()

built_in_functions = [Sin, Cos, Tan, Asin, Acos, Atan, Exp, Ln]