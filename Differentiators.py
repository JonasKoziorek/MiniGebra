from Atoms import *

class BinaryDifferentiator:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivisionDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return (self.left.diff() * self.right - self.left * self.right.diff()) / (self.right ** Number(2))

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

class ExponentiationDifferentiator(BinaryDifferentiator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def diff(self):
        return Exp([self.right * Ln([self.left])]).diff()