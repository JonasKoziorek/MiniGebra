class Command:
    """
    User can affect the behaviour of the interpreter through commands.
    Commands are written this way:

        "command: param1, param2, param..."

    This format has to be followed. Commands are written to the input line where expressions are written.
    Close each command and expression with ; symbol:

        "command1: param1";"command2: param1, param2";expr
    """
    name = ""
    def __init__(self, text: str):
        self.text = text
        self.params = self.parse_params(text)

    def __repr__(self) -> str:
        """
        Converts an instance to string representation.
        """
        return f"{self.name}: {self.text}"

    def parse_params(self, text: str) -> str:
        """
        Converts parameters to a list of parameters.
        Eg. "  a,b,c " -> ["a", "b", "c"]
        """
        return text.strip().split(",")


class Domain(Command):
    """
    Usage:

        "domain: (a,b)" - plots will be plotted on the range from a to b.
    
    Example:

        "domain: (-5, 10)"

    """
    name = "domain"
    def __init__(self, text:str):
        super().__init__(text)

class Vars(Command):
    """
    Usage:

        "vars: var1, var2, var3, ..." - specifies variable names in the math expressions

    Example:

        "vars: x, y, abc" - each string (x,y, abc) is now treated as a variable in math expressions

    """
    name = "vars"
    def __init__(self, text:str):
        super().__init__(text)

class Params(Command):
    """
    Usage:

        "params: param1, param2, param3, ..." - specifies parameter names in the math expressions

    Example:

        "params: a, b, c" - each string (a,b,c) is now treated as a parameter in math expressions !! this feature is not implemented yet

    """
    name = "params"
    def __init__(self, text:str):
        super().__init__(text)

class DiffOrder(Command):
    """
    Usage:

        "diff_order: integer" - specifies number of desired derivations of the math expression

    Example:

        "diff_order: 3" - this means that interpreter will produce up to third order derivatives of the math expression

    """
    name = "diff_order"
    def __init__(self, text:str):
        super().__init__(text)

class Precision(Command):
    """
    Usage:

        "precision: float" - specifies precision of plotting / size of a step in the domain 

    Example:

        "precision: 0.1" - if the domain was for example (0,1) this would mean that the domain would be discretized to [0, 0.1, 0.2, ..., 1], precision plays a role of a step

    """
    name = "precision"
    def __init__(self, text:str):
        super().__init__(text)

VALID_COMMANDS = [Domain, Vars, Params, DiffOrder, Precision]
VALID_NAMES = [i.name for i in VALID_COMMANDS]