import Atoms as Atoms
from Errors import DifferentiationError

class BinaryDifferentiator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivisionDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Atoms.Number(2))

class MultiplicationDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() * self.right + self.left * self.right.diff()

class PlusDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() + self.right.diff()

class MinusDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return self.left.diff() - self.right.diff()

class ExponentiationiationDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return Atoms.Exp([self.right * Atoms.Ln([self.left])]).diff()

class FunctionDifferentiator:
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

class SinDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Cos([arg]) * arg.diff()
        else:
            self._error_message()

class CosDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(-1) * Atoms.Sin([arg]) * arg.diff()
        else:
            self._error_message()

class TanDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(1) / (Atoms.Cos(self.args)*Atoms.Cos(self.args)) * arg.diff()
        else:
            self._error_message()

class AsinDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class AcosDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class AtanDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        # to be added
        return self

class ExpDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Exp(arg) * arg.diff()
        else:
            self._error_message()

class LnDifferentiator(FunctionDifferentiator):
    def __init__(self, name, args):
        super().__init__(name, args)

    def diff(self):
        if len(self.args) == 1:
            arg = self.args[0]
            return Atoms.Number(1) / arg * arg.diff()
        else:
            self._error_message()
