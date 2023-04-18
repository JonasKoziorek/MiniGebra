import Atoms as Atoms

class Atom:
    def __init__(self, parent):
        self.parent = parent

    def string_format(self):
        return "atom"

    def latex_format(self):
        return self.string_format()

    def mathjax_format1(self):
        return "$" + self.latex_format() + "$"

    def mathjax_format2(self):
        return "$$" + self.latex_format() + "$$"

class Var(Atom):
    def __init__(self, value, parent):
        super().__init__(parent)
        self.value = value

    def string_format(self):
        return f"{self.value}"

class Num(Atom):
    def __init__(self, value, parent):
        super().__init__(parent)
        self.value = value

    def string_format(self):
        return f"{self.value}"

class BinaryOperator(Atom):
    def __init__(self, left, right, parent):
        super().__init__(parent)
        self.left = left
        self.right = right

    def string_format(self):
        return f"operator({self.left},{self.right})"

class Div(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        left, right = self.__correct_bracket(self.left, self.right)
        return f"{left} / {right}"

    def latex_format(self):
        left, right = self.__correct_bracket(self.left.print("latex"), self.right.print("latex"))
        return r"\frac{" + str(left) + "}{" + str(right) + "}"

    def __correct_bracket(self, left, right):
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Div, Atoms.Expon]
        if type(self.left) in bracket_types:
            left = f"({left})"

        if type(self.right) in bracket_types:
            right = f"({right})"

        return left, right



class Mul(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        left = self.left ; right = self.right
        left = self.left ; right = self.right
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Expon, Atoms.Div]
        neglect_types = [Atoms.Function, Atoms.Var, Atoms.Num, *Atoms.built_in_functions]
        if type(left) == Atoms.Num and type(right) == Atoms.Num:
            if left.num < 0:
                return f"({left} * {right})"
            else:
                return f"{left} * {right}"

        if type(left) in neglect_types and type(right) in neglect_types:
            if type(left) == Atoms.Num and left.num < 0:
                return f"({self.left}{self.right})"
            elif type(right) == Atoms.Num and right.num < 0:
                return f"({self.right}{self.left})"
            else:
                return f"{self.left}{self.right}"

        if type(left) in bracket_types:
            left = f"({left})"

        if type(right) in bracket_types:
            right = f"({right})"

        return f"{left}{right}"

    def latex_format(self):
        left = self.left.print("latex") ; right = self.right.print("latex")
        bracket_types = [Atoms.Plus, Atoms.Minus, Atoms.Expon, Atoms.Div]
        neglect_types = [Atoms.Function, Atoms.Var, Atoms.Num, *Atoms.built_in_functions]
        if type(self.left) == Atoms.Num and type(self.right) == Atoms.Num:
            if self.left.num < 0:
                return f"({left}"+ r" \cdot " +  f"{right})"
            else:
                return f"{left}"+ r" \cdot " +  f"{right}"

        if type(self.left) in neglect_types and type(self.right) in neglect_types:
            if type(self.left) == Atoms.Num and self.left.num < 0:
                return f"({left}{right})"
            elif type(self.right) == Atoms.Num and self.right.num < 0:
                return f"({right}{left})"
            else:
                return f"{left}{right}"

        if type(self.left) in bracket_types:
            left = f"({left})"

        if type(self.right) in bracket_types:
            right = f"({right})"

        return f"{left}{right}"

        
class Plus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        return f"{self.left} + {self.right}"

    def latex_format(self):
        return f"{self.left.print('latex')} + {self.right.print('latex')}"

class Minus(BinaryOperator):
    def __init__(self, left, right, parent):
        super().__init__(left, right, parent)
    
    def string_format(self):
        return f"{self.left} - {self.right}"

    def latex_format(self):
        return f"{self.left.print('latex')} - {self.right.print('latex')}"

class Expon(BinaryOperator):
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

    def latex_format(self):
        left = self.left.print('latex')
        right = self.right.print('latex')
        if isinstance(self.right, Atoms.BinaryOperator):
            right = f"({self.right})"

        if isinstance(self.left, Atoms.BinaryOperator):
            left = f"({self.left})"

        return f"{left}" +  r"^{" f"{right}" + "}"

class Function(Atom):
    def __init__(self, name, args, parent):
        super().__init__(parent)
        self.name = name
        self.args = args

    def string_format(self):
        return f"{self.name}({self.__string_args_format()})"

    def __string_args_format(self):
        string = str(self.args[0])
        string = string + "".join([f", {str(arg)}" for arg in self.args[1:]])
        return string

    def _latex_args_format(self):
        string = self.args[0].print('latex')
        string = string + "".join([f", {arg.print('latex')}" for arg in self.args[1:]])
        return string

class Sin(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def latex_format(self):
        return r"\sin{" + self._latex_args_format() + "}"

class Cos(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def latex_format(self):
        return r"\cos{" + self._latex_args_format() + "}"

class Tan(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def latex_format(self):
        return r"\tan{" + self._latex_args_format() + "}"

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

    def latex_format(self):
        return r"e^{" + self._latex_args_format() + "}"

class Ln(Function):
    def __init__(self, name, args, parent):
        super().__init__(name, args, parent)

    def latex_format(self):
        return r"\ln{" + self._latex_args_format() + "}"