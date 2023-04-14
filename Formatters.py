import Atoms as Atoms

class Binary:
    def __init__(self, left, right, parent):
        self.left = left
        self.right = right
        self.parent = parent

class Div(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        left = self.left ; right = self.right
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Div, Atoms.Expon]
        if type(left) in bracket_types:
            left = f"({self.left})"

        if type(right) in bracket_types:
            right = f"({self.right})"

        return f"{left} / {right}"

class Mul(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        left = self.left ; right = self.right
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Expon, Atoms.Div]
        neglect_types = [Atoms.Function, Atoms.Variable, Atoms.Number, *Atoms.built_in_functions]
        if type(left) == Atoms.Number and type(right) == Atoms.Number:
            if left.num < 0:
                return f"({left} * {right})"
            else:
                return f"{left} * {right}"

        if type(left) in neglect_types and type(right) in neglect_types:
            if type(left) == Atoms.Number and left.num < 0:
                return f"({self.left}{self.right})"
            elif type(right) == Atoms.Number and right.num < 0:
                return f"({self.right}{self.left})"
            else:
                return f"{self.left}{self.right}"

        if type(left) in bracket_types:
            left = f"({left})"

        if type(right) in bracket_types:
            right = f"({right})"

        return f"{left}{right}"

class Plus(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        return f"{self.left} + {self.right}"

class Minus(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        return f"{self.left} - {self.right}"

class Expon(Binary):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        left = str(self.left)
        right = str(self.right)
        if isinstance(self.right, Atoms.BinaryOperator):
            right = f"({self.right})"

        if isinstance(self.left, Atoms.BinaryOperator):
            left = f"({self.left})"

        return f"{left} ^ {right}"

class Function:
    def __init__(self, name, args, parent):
        self.name = name
        self.args = args
        self.parent = parent

    def string_format(self):
        string = str(self.args[0])
        string = string + "".join([f", {str(arg)}" for arg in self.args[1:]])
        return f"{self.name}({string})"
