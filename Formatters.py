import Atoms as Atoms

class BinaryFormatter:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivisionFormatter(BinaryFormatter):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def string_format(self):
        left = self.left ; right = self.right
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Division, Atoms.Exponentiation]
        if type(left) in bracket_types:
            left = f"({self.left})"

        if type(right) in bracket_types:
            right = f"({self.right})"

        return f"{left} / {right}"

class MultiplicationFormatter(BinaryFormatter):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def string_format(self):
        left = self.left ; right = self.right
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Exponentiation, Atoms.Division]
        neglect_types = [Atoms.Number, Atoms.Function, Atoms.Variable]
        if type(left) in neglect_types and type(right) == Atoms.Variable:
            return f"{self.left}{self.right}"

        if type(left) == Atoms.Number and type(right) == Atoms.Number:
            return f"{left} * {right}"

        if type(left) in bracket_types:
            left = f"({left})"

        if type(right) in bracket_types:
            right = f"({right})"

        return f"{left}{right}"

class PlusFormatter(BinaryFormatter):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def string_format(self):
        return f"{self.left} + {self.right}"

class MinusFormatter(BinaryFormatter):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def string_format(self):
        return f"{self.left} - {self.right}"


class ExponentiationFormatter(BinaryFormatter):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def string_format(self):
        left = str(self.left)
        right = str(self.right)
        if isinstance(self.right, Atoms.BinaryOperator):
            right = f"({self.right})"

        if isinstance(self.left, Atoms.BinaryOperator):
            left = f"({self.left})"

        return f"{left} ^ {right}"


class FunctionFormatter:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def string_format(self):
        string = str(self.args[0])
        string = string.join([f", {str(arg)}" for arg in self.args[1:]])
        return f"{self.name}({string})"
