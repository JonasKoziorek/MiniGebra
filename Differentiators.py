import Atoms as Atoms
from Errors import DifferentiationError

class Binary:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Division(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Atoms.Number(2))

class Multiplication(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

class Plus(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() + self.right.diff()

class Minus(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() - self.right.diff()

class Exponentiation(Binary):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return Atoms.Exp([self.right * Atoms.Ln([self.left])]).diff()

class Function:
    def __init__(self,name, args):
        self.name = name
        self.args = args

    def _error_message(self):
        raise DifferentiationError(f"Function {self.name} only supports single variable differentiating.")

    def diff(self):
        if len(self.args) == 1:
            return self * self.args[0].diff()
        else:
            self._error_message()

class Sin(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Cos([arg]) * arg.diff()
        else:
            self._error_message()

class Cos(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(-1) * Atoms.Sin([arg]) * arg.diff()
        else:
            self._error_message()

class Tan(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(1) / (Atoms.Cos(self.args)*Atoms.Cos(self.args)) * arg.diff()
        else:
            self._error_message()

class Asin(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class Acos(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class Atan(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class Exp(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Exp(arg) * arg.diff()
        else:
            self._error_message()

class Ln(Function):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(1) / arg * arg.diff()
        else:
            self._error_message()
