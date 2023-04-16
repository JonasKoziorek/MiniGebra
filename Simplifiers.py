import Atoms as Atoms
from numpy import gcd

class Atom:
    def __init__(self, parent):
        self.parent = parent

    def _simplify_list(self, list_, operation):
        if len(list_) > 1:
            elem = list_[0]
            rest = list_[1:]
            for index, atom in enumerate(rest):
                simplification = operation(elem, atom).simplify_expr()
                if type(simplification) != operation:
                    list_[index+1] = simplification
                    list_ = self._simplify_list(list_[1:], operation)
                    return list_
            return [elem] + self._simplify_list(rest, operation)
        else:
            return list_

    def simplify_list(self):
        return self.parent.to_ast(self._simplify_list(self.parent.to_list(), type(self.parent)))

    def simplify_expr(self):
        return self.parent

    def simplify(self):
        simplifier = self.simplify_expr().get_simplifier()
        return simplifier.simplify_list()

class Var(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

class Num(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

class BinaryOperator(Atom):
    def __init__(self, left, right, parent):
        super().__init__(parent)
        self.left = left
        self.right = right

class Div(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def simplify_expr(self):
        left = self.left
        right = self.right
        # 0 / expr = 0
        if left == 0:
            return Atoms.Num(0)

        # expr / 1 = expr
        elif right == 1:
            return left.simplify()

        # reduce fraction
        elif type(left) == Atoms.Num and type(right) == Atoms.Num:
            a = left.num
            b = right.num
            if type(a) == int and type(b) == int:
                div = gcd(a,b)
                a = Atoms.Num(int(a/div))
                b = Atoms.Num(int(b/div))
                return a / b

        else:
            return left.simplify() / right.simplify()

class Mul(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def _isNumMul(self, left, right):
        if type(left) == Atoms.Num and type(right) == Atoms.Num:
            return True
        else:
            return False

    def isNumMul(self):
        return self._isNumMul(self.left, self.right)
    
    def simplify_expr(self):
        left = self.left
        right = self.right
        # 0 * expr = 0
        if left == 0:
            return Atoms.Num(0)

        # expr * 0 = 0
        elif right == 0:
            return Atoms.Num(0)

        # 1 * expr = expr
        elif left == 1:
            return right.simplify()

        # expr * 1 = expr
        elif right == 1:
            return left.simplify()

        # expr * constant = constant * expr
        elif type(right) == Atoms.Num and type(left) != Atoms.Num:
            return right * left.simplify()

        # a/b * c/d = (a*c)/(b*d)
        elif type(left) == Atoms.Div and type(right) == Atoms.Div:
            a = left.left ; b = left.right
            c = right.left ; d = right.right
            return (a.simplify() * c.simplify()) / (b.simplify() * d.simplify())

        # expr ^ a * expr ^ b = expr ^ (a+b)
        elif type(left) == Atoms.Expon and type(right) == Atoms.Expon:
            if type(left.right) == Atoms.Num and type(right.right) == Atoms.Num and str(left.left) == str(right.left):
                expr = left.left
                a = left.right ; b = right.right
                return expr ** (a + b)
            else:
                return left.simplify() * right.simplify()

        # a * (b * x) = (a*b)*x
        elif type(left) == Atoms.Num and type(right) == Atoms.Mul and type(right.left) == Atoms.Num:
            a = left ; b = right.left ; x = right.right
            return (a*b) * x

        # a * (b/c) = (a*b)/c
        elif type(left) == Atoms.Num and type(right) == Atoms.Div and type(right.left) == Atoms.Num:
            a = left ; b = right.left ; c = right.right
            return (a*b) / c.simplify()

        # (b/c)*a = (a*b)/c
        elif type(right) == Atoms.Num and type(left) == Atoms.Div and type(left.left) == Atoms.Num:
            b = left.left ; c = left.right ; a = right
            return (a*b) / c.simplify()

        # (a^b) * expr = expr * (a^b) # changing order
        elif type(left) == Atoms.Expon and type(right) != Atoms.Expon:
            return right * left
        
        # a * ((b*c)*expr) = (a*b*c)*expr
        elif type(left) == Atoms.Num and type(right) == Atoms.Mul and type(right.left) == Atoms.Mul and self._isNumMul(right.left.left, right.left.right):
            a = left
            b = right.left.left
            c = right.left.right
            expr = right.right
            return (a*b*c) * expr.simplify()

        # a * (expr*(b*c)) = (a*b*c)*expr
        elif type(left) == Atoms.Num and type(right) == Atoms.Mul and type(right.right) == Atoms.Mul and self._isNumMul(right.right.left, right.right.right):
            a = left
            expr = right.left
            b = right.right.left
            c = right.right.right
            return (a*b*c) * expr.simplify()

        # (expr*(b*c))*a = (a*b*c)*expr
        elif type(right) == Atoms.Num and type(left) == Atoms.Mul and type(left.right) == Atoms.Mul and self._isNumMul(left.right.left, left.right.right):
            a = right
            b = left.right.left
            c = left.right.right
            expr = left.left
            return (a*b*c) * expr.simplify() 

        # ((b*c)*expr)*a = (a*b*c)*expr
        elif type(right) == Atoms.Num and type(left) == Atoms.Mul and type(left.left) == Atoms.Mul and self._isNumMul(left.left.left, left.left.right):
            a = right
            b = left.left.left
            c = left.left.right
            expr = left.right
            return (a*b*c) * expr.simplify()

        # expr * expr = expr^2
        elif str(left) == str(right):
            expr = left
            return expr ** 2

        # expr * expr ^ a
        elif type(right) == Atoms.Expon and str(left) == str(right.left):
            expr = left.simplify()
            a = right.right
            return expr ** (a + 1)

        # (a/x)(x^b) = ax^(b-1)
        elif type(left) == Atoms.Div and type(right) == Atoms.Expon and str(left.right) == str(right.left) and type(right.right) == Atoms.Num:
            a = left.left
            x = left.right
            b = right.right
            return a * (x ** (b - 1).simplify())

        else:
            return left.simplify() * right.simplify()
            
class Plus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def simplify_expr(self):
        left = self.left
        right = self.right
        # 0 + expr = expr
        if left == 0:
            return right.simplify()

        # expr + 0 = expr
        elif right == 0:
            return left.simplify()

        # ln a + ln b = ln (a*b)
        elif type(left) == Atoms.Ln and type(right) == Atoms.Ln and len(left.args) == 1 and len(right.args) == 1:
            return Atoms.Ln(left.args[0].simplify() * right.args[0].simplify())

        # a * x + x = (a+1) * x
        elif type(left) == Atoms.Mul and type(left.left) == Atoms.Num and str(left.right) == str(right):
            return (left.left + 1) * left.right

        # expr + expr = 2*expr
        elif str(left) == str(right):
            return left * 2

        # a*expr + b*expr = (a+b) * expr
        elif type(left) == Atoms.Mul and type(right) == Atoms.Mul:
            if type(left.left) == Atoms.Num and type(right.left) == Atoms.Num and str(left.right) == str(right.right):
                return (left.left + right.left) * left.right.simplify()
            else:
                return left.simplify() + right.simplify()

        else:
            return left.simplify() + right.simplify()
    
class Minus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def simplify_expr(self):
        left = self.left
        right = self.right
        # 0 - expr = expr
        if left == 0:
            return Atoms.Num(-1) * right.simplify()

        # expr - 0 = expr
        elif right == 0:
            return left.simplify()

        # expr - expr = 0
        elif str(left) == str(right):
            return Atoms.Num(0)

        # ln a - ln b = ln (a/b)
        elif type(left) == Atoms.Ln and type(right) == Atoms.Ln and len(left.args) == 1 and len(right.args) == 1:
            return Atoms.Ln(left.args[0].simplify() / right.args[0].simplify())

        # a*var - b*var = (a-b) * var
        elif type(left) == Atoms.Mul and type(right) == Atoms.Mul:
            if type(left.left) == Atoms.Num and type(right.left) == Atoms.Num and str(left.right) == str(right.right):
                return (left.left - left.right) * left.right.simplify()
            else:
                return left.simplify() - right.simplify()
        else:
            return left.simplify() - right.simplify()

class Expon(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def simplify_expr(self):
        left = self.left
        right = self.right

        # expr ^ 1 = expr
        if type(right) == Atoms.Num and right == 1:
            return left.simplify()

        # expr ^ 0 = 1
        elif type(right) == Atoms.Num and right == 0:
            return Atoms.Num(1)

        # ((x ^ a) ^ b) = x ^ (a*b)
        elif type(left) == Atoms.Expon and type(right) == Atoms.Num:
            if type(left.right) == Atoms.Num:
                return left.left.simplify() ** (left.right * right)
            else:
                return left.simplify() ** right.simplify()

        else:
            return left.simplify() ** right.simplify()

class Function(Atom):
    def __init__(self, name, args, parent):
        super().__init__(parent)
        self.name = name
        self.args = args

    def simplify_expr(self):
        class_ = type(self.parent)
        if class_ in Atoms.built_in_functions:
            return class_([a.simplify() for a in self.args])
        else:
            return class_(self.name, [a.simplify() for a in self.args])

class Sin(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Cos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Tan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Asin(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Acos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Atan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

class Exp(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)
    
    def simplify_expr(self):
        if len(self.args) == 1:
            arg = self.args[0]
            if type(arg) == Atoms.Mul and type(arg.right) == Atoms.Ln and len(arg.right.args) == 1:
                return Atoms.Expon(arg.right.args[0].simplify(), arg.left.simplify())
            else:
                return self.parent
        else:
            return self.parent

class Ln(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def simplify_expr(self):
        args = self.args
        # ln a^b = b * ln a
        if len(args) == 1 and type(args[0]) == Atoms.Expon:
            return args[0].right.simplify() * Atoms.Ln([args[0].left.simplify()])
        else:
            return self.parent
