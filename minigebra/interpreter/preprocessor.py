# for type hinting
from ..interpreter.commands import Command
from ..interpreter.atoms import Atom


class Preprocessor:
    """
    This module modifies interpreter input so that it is easier to process it.
    """

    def __init__(self, input: str):
        self.input = input

    def preprocess(self) -> tuple[list[Command], list[Atom]]:
        """
        Separate input string to list of expressions and list of commands.
        """
        exprs = self.split_to_exprs()
        commands = list(filter(self.check_for_commands, exprs))
        exprs = list(filter(lambda x: x not in commands, exprs))
        return commands, exprs

    def split_to_exprs(self) -> list[str]:
        """
        Separate input string to individual expressions which are separated by ';' character.
        """
        lst = [string.strip() for string in self.input.split(";")]
        return list(filter(lambda x: bool(x), lst))

    def check_for_commands(self, expr_str) -> bool:
        """
        Check if the expression is enclosed by double quotes.
        """
        if expr_str[0] == '"' and expr_str[-1] == '"':
            return True
        return False