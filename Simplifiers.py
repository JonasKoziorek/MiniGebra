from Atoms import *

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

class BinarySimplifier:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivisionSimplifier(BinarySimplifier):
    def __init__(self, left, right):
        super().__init__(left, right)
    
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

class MultiplicationSimplifier(BinarySimplifier):
    def __init__(self, left, right):
        super().__init__(left, right)

    def _isNumMul(self, left, right):
        if type(left) == Number and type(right) == Number:
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

        # a * (b/c) = (a*b)/c
        elif type(left) == Number and type(right) == Division and type(right.left) == Number:
            return Division(left*right.left, right.right.simplify())

        # (b/c)*a = (a*b)/c
        elif type(right) == Number and type(left) == Division and type(left.left) == Number:
            return Division(right*left.left, left.right.simplify())

        # (a^b) * (c*/d) = (c*/d) * (a^b)
        elif type(left) == Exponentiation and (type(right) == Multiplication or type(right) == Division):
            return Multiplication(right, left)
        
        # a * ((b*c)*expr) = (a*b*c)*expr
        elif type(left) == Number and type(right) == Multiplication and type(right.left) == Multiplication and self._isNumMul(right.left.left, right.left.right):
            return Multiplication(left * right.left.left * right.left.right, right.right.simplify())

        # a * (expr*(b*c)) = (a*b*c)*expr
        elif type(left) == Number and type(right) == Multiplication and type(right.right) == Multiplication and self._isNumMul(right.right.left, right.right.right):
            return Multiplication(left * right.right.left * right.right.right, right.left.simplify())

        # (expr*(b*c))*a = (a*b*c)*expr
        elif type(right) == Number and type(left) == Multiplication and type(left.right) == Multiplication and self._isNumMul(left.right.left, left.right.right):
            return Multiplication(right * left.right.left * left.right.right, left.left.simplify())

        # ((b*c)*expr)*a = (a*b*c)*expr
        elif type(right) == Number and type(left) == Multiplication and type(left.left) == Multiplication and self._isNumMul(left.left.left, left.left.right):
            return Multiplication(right * left.left.left * left.left.right, left.right.simplify())

        else:
            return Multiplication(left.simplify(), right.simplify())

    
class PlusSimplifier(BinarySimplifier):
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
    
class MinusSimplifier(BinarySimplifier):
    def __init__(self, left, right):
        super().__init__(left, right)

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

class ExponentiationSimplifier(BinarySimplifier):
    def __init__(self, left, right):
        super().__init__(left, right)

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

class FunctionSimplifier:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def simplify(self):
        # func(expr) = func(expr.simplify())
        class_ = type(self)
        if class_ in built_in_functions:
            return class_([a.simplify() for a in self.args])
        else:
            return class_(self.name, [a.simplify() for a in self.args])

class ExpSimplifier:
    def __init__(self, args):
        self.args = args
    
    def simplify(self):
        if len(self.args) == 1:
            arg = self.args[0]
            if type(arg) == Multiplication and type(arg.right) == Ln and len(arg.right.args) == 1:
                return Exponentiation(arg.right.args[0].simplify(), arg.left.simplify())
            else:
                return self
        else:
            return self

class LnSimplifier:
    def __init__(self, args):
        self.args = args

    def simplify(self):
        args = self.args
        # ln a^b = b * ln a
        if len(args) == 1 and type(args[0]) == Exponentiation:
            return args[0].right.simplify() * Ln([args[0].left.simplify()])
        else:
            return self
