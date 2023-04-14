import Atoms as Atoms
from Errors import DifferentiationError

class Binary:
    def __init__(self, left, right, parent):
        self.left = left
        self.right = right
        self.parent = parent

class Div(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Atoms.Number(2))

class Mul(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

class Plus(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() + self.right.diff()

class Minus(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return self.left.diff() - self.right.diff()

class Expon(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)

    def diff(self):
        return Atoms.Exp([self.right * Atoms.Ln([self.left])]).diff()

class Function:
    def __init__(self,name, args, parent):
        self.name = name
        self.args = args
        self.parent = parent

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
            return Atoms.Number(-1) * Atoms.Sin([arg]) * arg.diff()
        else:
            self._error_message()

class Tan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(1) / (Atoms.Cos(self.args)*Atoms.Cos(self.args)) * arg.diff()
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
            return Atoms.Number(1) / arg * arg.diff()
        else:
            self._error_message()
