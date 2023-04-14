import Atoms as Atoms
# from Atoms import (Atom,
#                    BinaryOperator,
#                    Atoms.Divisionvision,
#                    Atoms.Multiplication,
#                    Atoms.Plus,
#                    Atoms.Minus,
#                    Atoms.Number,
#                    Atoms.Variable,
#                    Function,
#                    Sin,
#                    Cos,
#                    Tan,
#                    Exp,
#                    Atoms.Ln,
#                    Atoms.Exponentiation,
#                    built_in_functions)

from numpy import gcd

# some of the applied simplifications
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

class Binary:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Division(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def simplify(self):
        left = self.left
        right = self.right
        # 0 / expr = 0
        if left == 0:
            return Atoms.Number(0)

        # expr / 1 = expr
        elif right == 1:
            return left.simplify()

        # # const / const = const/const
        # elif type(left) == Atoms.Number and type(right) == Atoms.Number:
        #     return Atoms.Number(left.num / right.num)

        # reduce fraction
        elif type(left) == Atoms.Number and type(right) == Atoms.Number:
            a = left.num
            b = right.num
            if type(a) == int and type(b) == int:
                div = gcd(a,b)
                a = Atoms.Number(int(a/div))
                b = Atoms.Number(int(b/div))
                return Atoms.Divisionvision(a,b)

        else:
            return Atoms.Divisionvision(left.simplify(), right.simplify())

class Multiplication(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def _isNumMul(self, left, right):
        if type(left) == Atoms.Number and type(right) == Atoms.Number:
            return True
        else:
            return False

    def isNumMul(self):
        return self._isNumMul(self.left, self.right)
    
    def simplify(self):
        left = self.left
        right = self.right
        # 0 * expr = 0
        if left == 0:
            return Atoms.Number(0)

        # expr * 0 = 0
        elif right == 0:
            return Atoms.Number(0)

        # 1 * expr = expr
        elif left == 1:
            return right.simplify()

        # expr * 1 = expr
        elif right == 1:
            return left.simplify()

        # expr * constant = constant * expr
        elif type(right) == Atoms.Number and type(left) != Atoms.Number:
            return right * left.simplify()

        # const * const = const*const
        elif type(left) == Atoms.Number and type(right) == Atoms.Number:
            return Atoms.Number(left.num * right.num)

        # a/b * c/d = (a*c)/(b*d)
        elif type(left) == Atoms.Division and type(right) == Atoms.Division:
            return Atoms.Divisionvision(left.left.simplify() * right.left.simplify(), left.right.simplify() * right.right.simplify())

        # expr ^ a * expr ^ b = expr ^ (a+b)
        elif type(left) == Atoms.Exponentiation and type(right) == Atoms.Exponentiation:
            if type(left.right) == Atoms.Number and type(right.right) == Atoms.Number and str(left.left) == str(right.left):
                return Atoms.Exponentiation(left.left.simplify(), left.right.num * right.right.num)
            else:
                return self

        # a * (b * x) = (a*b)*x
        elif type(left) == Atoms.Number and type(right) == Atoms.Multiplication and type(right.left) == Atoms.Number:
            return Atoms.Multiplication(Atoms.Number(left.num * right.left.num), right.right.simplify())

        # a * (b/c) = (a*b)/c
        elif type(left) == Atoms.Number and type(right) == Atoms.Division and type(right.left) == Atoms.Number:
            return Atoms.Divisionvision(left*right.left, right.right.simplify())

        # (b/c)*a = (a*b)/c
        elif type(right) == Atoms.Number and type(left) == Atoms.Division and type(left.left) == Atoms.Number:
            return Atoms.Divisionvision(right*left.left, left.right.simplify())

        # (a^b) * (c*/d) = (c*/d) * (a^b)
        elif type(left) == Atoms.Exponentiation and (type(right) == Atoms.Multiplication or type(right) == Atoms.Divisionvision):
            return Atoms.Multiplication(right, left)
        
        # a * ((b*c)*expr) = (a*b*c)*expr
        elif type(left) == Atoms.Number and type(right) == Atoms.Multiplication and type(right.left) == Atoms.Multiplication and self._isNumMul(right.left.left, right.left.right):
            return Atoms.Multiplication(left * right.left.left * right.left.right, right.right.simplify())

        # a * (expr*(b*c)) = (a*b*c)*expr
        elif type(left) == Atoms.Number and type(right) == Atoms.Multiplication and type(right.right) == Atoms.Multiplication and self._isNumMul(right.right.left, right.right.right):
            return Atoms.Multiplication(left * right.right.left * right.right.right, right.left.simplify())

        # (expr*(b*c))*a = (a*b*c)*expr
        elif type(right) == Atoms.Number and type(left) == Atoms.Multiplication and type(left.right) == Atoms.Multiplication and self._isNumMul(left.right.left, left.right.right):
            return Atoms.Multiplication(right * left.right.left * left.right.right, left.left.simplify())

        # ((b*c)*expr)*a = (a*b*c)*expr
        elif type(right) == Atoms.Number and type(left) == Atoms.Multiplication and type(left.left) == Atoms.Multiplication and self._isNumMul(left.left.left, left.left.right):
            return Atoms.Multiplication(right * left.left.left * left.left.right, left.right.simplify())

        else:
            return Atoms.Multiplication(left.simplify(), right.simplify())

    
class Plus(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

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
        elif type(left) == Atoms.Number and type(right) == Atoms.Number:
            return Atoms.Number(left.num + right.num)

        # var + var = (2) * var
        elif type(left) == Atoms.Variable and type(right) == Atoms.Variable and left.value == right.value:
                return Atoms.Number(2) * right

        # a*var + b*var = (a+b) * var
        elif type(left) == Atoms.Multiplication and type(right) == Atoms.Multiplication:
            if type(left.left) == Atoms.Number and type(right.left) == Atoms.Number and str(left.right) == str(right.right):
                return Atoms.Number(left.left + left.right) * left.right.simplify()
            else:
                return Atoms.Plus(left.simplify(), right.simplify())

        # ln a + ln b = ln (a*b)
        elif type(left) == Atoms.Ln and type(right) == Atoms.Ln and len(left.args) == 1 and len(right.args) == 1:
            return Atoms.Ln(left.args[0].simplify() * right.args[0].simplify())

        else:
            return Atoms.Plus(left.simplify(), right.simplify())
    
class Minus(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def simplify(self):
        left = self.left
        right = self.right
        # 0 - expr = expr
        if left == 0:
            return Atoms.Number(-1) * right.simplify()

        # expr - 0 = expr
        elif right == 0:
            return left.simplify()

        # const - const = const-const
        elif type(left) == Atoms.Number and type(right) == Atoms.Number:
            return Atoms.Number(left.num + right.num)

        # ln a - ln b = ln (a/b)
        elif type(left) == Atoms.Ln and type(right) == Atoms.Ln and len(left.args) == 1 and len(right.args) == 1:
            return Atoms.Ln(left.args[0].simplify() / right.args[0].simplify())

        # var - var = 0
        elif type(left) == Atoms.Variable and type(right) == Atoms.Variable and left.value == right.value:
                return Atoms.Number(0)

        # a*var - b*var = (a-b) * var
        elif type(left) == Atoms.Multiplication and type(right) == Atoms.Multiplication:
            if type(left.left) == Atoms.Number and type(right.left) == Atoms.Number and str(left.right) == str(right.right):
                return (left.left - left.right) * left.right.simplify()
            else:
                return Atoms.Minus(left.simplify(), right.simplify())

        else:
            return Atoms.Minus(left.simplify(), right.simplify())

class Exponentiation(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def simplify(self):
        left = self.left
        right = self.right

        # expr ^ 1 = expr
        if type(right) == Atoms.Number and right == 1:
            return left.simplify()

        # expr ^ 0 = 1
        elif type(right) == Atoms.Number and right == 0:
            return Atoms.Number(1)

        # ((x ^ a) ^ b) = x ^ (a*b)
        elif type(left) == Atoms.Exponentiation and type(right) == Atoms.Number:
            if type(left.right) == Atoms.Number:
                return Atoms.Exponentiation(left.left.simplify(), left.right * right)
            else:
                return self

        # a ^ b = a^b
        elif type(left) == Atoms.Number and type(right) == Atoms.Number:
            return Atoms.Number(left.num ** right.num)

        else:
            return self

class Function:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def simplify(self):
        # func(expr) = func(expr.simplify())
        class_ = type(self)
        if class_ in Atoms.built_in_functions:
            return class_([a.simplify() for a in self.args])
        else:
            return class_(self.name, [a.simplify() for a in self.args])

class Exp:
    def __init__(self, args):
        self.args = args
    
    def simplify(self):
        if len(self.args) == 1:
            arg = self.args[0]
            if type(arg) == Atoms.Multiplication and type(arg.right) == Atoms.Ln and len(arg.right.args) == 1:
                return Atoms.Exponentiation(arg.right.args[0].simplify(), arg.left.simplify())
            else:
                return self
        else:
            return self

class Ln:
    def __init__(self, args):
        self.args = args

    def simplify(self):
        args = self.args
        # ln a^b = b * ln a
        if len(args) == 1 and type(args[0]) == Atoms.Exponentiation:
            return args[0].right.simplify() * Atoms.Ln([args[0].left.simplify()])
        else:
            return self
