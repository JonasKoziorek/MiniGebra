import Atoms as Atoms
from Errors import DifferentiationError

class Atom:
    def __init__(self, parent):
        self.parent = parent

    def diff(self):
        return self.parent

class Var(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

    def diff(self):
        return Atoms.Num(1)

class Num(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

    def diff(self):
        return Atoms.Num(0)

class BinaryOperator(Atom):
    def __init__(self, left, right, parent):
        super().__init__(parent)
        self.left = left
        self.right = right

class Div(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** 2)

class Mul(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

class Plus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() + self.right.diff()

class Minus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() - self.right.diff()

class Expon(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return Atoms.Exp([self.right * Atoms.Ln([self.left])]).diff()

class Function(Atom):
    def __init__(self,name, args, parent):
        super().__init__(parent)
        self.name = name
        self.args = args

    def _error_message(self):
        raise DifferentiationError(f"Function {self.name} only supports single variable differentiating.")

    def diff(self):
        if len(self.args) == 1:
            return self.parent * self.args[0].diff()
        else:
            self._error_message()

class Sin(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Cos([arg]) * arg.diff()
        else:
            self._error_message()

class Cos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Num(-1) * Atoms.Sin([arg]) * arg.diff()
        else:
            self._error_message()

class Tan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Num(1) / (Atoms.Cos(self.args)*Atoms.Cos(self.args)) * arg.diff()
        else:
            self._error_message()

class Asin(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        # to be added
        return self.parent

class Acos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        # to be added
        return self.parent

class Atan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        # to be added
        return self.parent

class Exp(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Exp(arg) * arg.diff()
        else:
            self._error_message()

class Ln(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Num(1) / arg * arg.diff()
        else:
            self._error_message()
