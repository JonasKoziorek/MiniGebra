from Atoms import *

class BinaryFormatter:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivisionFormatter(BinaryFormatter):
    def __init__(self, left, right)
        super().__init__(left, right)
    
    def string_format(self):

class MultiplicationFormatter(BinaryFormatter):
    def __init__(self, left, right)
        super().__init__(left, right)
    
    def string_format(self):

class PlusFormatter(BinaryFormatter):
    def __init__(self, left, right)
        super().__init__(left, right)
    
    def string_format(self):

class MinusFormatter(BinaryFormatter):
    def __init__(self, left, right)
        super().__init__(left, right)
    
    def string_format(self):

class ExponentiationFormatter(BinaryFormatter):
    def __init__(self, left, right)
        super().__init__(left, right)
    
    def string_format(self):
        left = str(self.left)
        right = str(self.right)
        if isinstance(self.right, BinaryOperator):
            right = f"({self.right})"

        if isinstance(self.left, BinaryOperator):
            left = f"({self.left})"

        return f"{left} ^ {right}"


class FunctionFormatter:
    def __init__(self, name, args)
        self.name = name
        self.args = args

    def string_format(self):
        string = str(self.args[0])
        string = string.join([f", {str(arg)}" for arg in self.args[1:]])
        return f"{self.name}({string})"

    
    def string_format(self):