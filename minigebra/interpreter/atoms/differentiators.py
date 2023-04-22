from . import atoms as atoms

class DifferentiationError(Exception):
    "Raised when an error occurs while differentiating."
    pass

class Atom:
    """
    Provides functions to symbolically differentiate atomic expressions.
    """
    def __init__(self, parent):
        self.parent = parent

    def diff(self):
        return self.parent

class Var(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

    def diff(self):
        return atoms.Num(1)

class Num(Atom):
    def __init__(self,value, parent):
        super().__init__(parent)
        self.value = value

    def diff(self):
        return atoms.Num(0)

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
        return atoms.Exp([self.right * atoms.Ln([self.left])]).diff()

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
            return atoms.Cos([arg]) * arg.diff()
        else:
            self._error_message()

class Cos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return atoms.Num(-1) * atoms.Sin([arg]) * arg.diff()
        else:
            self._error_message()

class Tan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return atoms.Num(1) / (atoms.Cos(self.args)*atoms.Cos(self.args)) * arg.diff()
        else:
            self._error_message()

class Exp(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return atoms.Exp(arg) * arg.diff()
        else:
            self._error_message()

class Ln(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return atoms.Num(1) / arg * arg.diff()
        else:
            self._error_message()
