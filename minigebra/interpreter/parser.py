from .atoms import Mul, Expon, Div, Plus, Minus, Var, Function, Num, Atom
from .commands import VALID_NAMES, VALID_COMMANDS, Command

# for type hinting
from .tokenizer import Tokenizer

class ParseError(Exception):
    "Raised when an error occurs while parsing."
    pass

class Parser:

    def __init__(self, tokenizer: Tokenizer, built_in_functions: list[Function]):
        self.tokenizer = tokenizer
        self.current = []
        self.built_in_functions = built_in_functions

    def parse_expr(self, string: str) -> Atom:
        """
        Parses expression from text.
        """
        self.tokenizer.read(string)
        self.current = self.tokenizer.next_match()
        try:
            return self.expression()
        except Exception as e:
            raise ParseError(f"Following error occured while parsing: {e}")

    def parse_command(self, command_str: str) -> Command:
        """
        Parses commands from text.
        """
        command = command_str[1:-1]
        tokens = command.split(":")
        if len(tokens) == 2:
            name = tokens[0]
            body = tokens[1]
            if name in VALID_NAMES:
                ind = VALID_NAMES.index(name)
                type_ = VALID_COMMANDS[ind]
                return type_(body)
            else:
                raise Exception(f"Unknown command {command}.\nAvailable commands are {VALID_NAMES}")
        else:
            raise ParseError(f"Command {command} is not valid.")

    def __determine_function(self, name: str, args: list[Atom]):
        """
        Checks whether a function belongs to built_in_functions.
        """
        names = [func.name for func in self.built_in_functions]
        try:
            index = names.index(name)
            func_type =  self.built_in_functions[index]
            return func_type(args)
        except ValueError:
            return Function(name, args)
    
    def advance(self) -> None:
        """
        Advances to next token.
        """
        self.current = self.tokenizer.next_match()

    def isToken(self, tokens: list[str]) -> bool:
        """
        Determines whether current token is in the tokens input list.
        """
        if self.current:
            return self.current["type"] in tokens

    def expression(self) -> Plus:
        return self.addition()

    def addition(self) -> Mul:
        """
        Determines whether token is a addition or substraction. Returns resulting token.
        """
        left = self.multiplication()

        while self.isToken(['PLUS', 'MINUS']):
            type = self.current["type"]
            self.advance()
            if type == "PLUS":
                left = Plus(left, self.multiplication())
            elif type == "MINUS":
                left = Minus(left, self.multiplication())

        return left

    def function(self) -> None:
        pass

    def multiplication(self) -> Expon:
        """
        Determines whether token is a multiplication or division. Returns resulting token.
        """
        left = self.exponentiation()

        while self.isToken(['MUL', 'DIV']):
            type = self.current["type"]
            self.advance()
            if type == "MUL":
                left = Mul(left, self.exponentiation())
            elif type == "DIV":
                left = Div(left, self.exponentiation())

        return left

    def exponentiation(self) -> Atom:
        """
        Determines whether token is a exponentiation. Returns resulting token.
        """
        left = self.basic()

        while self.isToken(['EXP']):
            self.advance()
            left = Expon(left, self.basic())

        return left

    def function(self) -> Atom:
        """
        Determines whether token is a function. Returns resulting token.
        """
        left = self.multiplication()

        if self.isToken(['LPAR']):
            self.advance()
            args = [self.expression()]

            while self.isToken(['COMMA']):
                self.advance()
                args.append(self.expression())

            self.advance()
            if type(left) == Var:
                return self.__determine_function(left.value, args)
                # return Function(left.value, args)
            else:
                raise Exception("Incorret function expression.")
        else:
            return left

    def basic(self) -> Atom:
        """
        Determines whether token is a variable, number, command or expr in parentheses. Returns resulting token.
        """
        tok = self.current

        if self.isToken(["VAR"]):
            self.advance()
            if self.isToken(['LPAR']):
                self.advance()
                args = [self.expression()]

                while self.isToken(['COMMA']):
                    self.advance()
                    args.append(self.expression())

                self.advance()
                name = Var(tok["token"]).value
                return self.__determine_function(name, args)
                # return Function(name, args)
            
            else:
                return Var(tok["token"])

        elif self.isToken(['LPAR']):
            self.advance()
            expr = self.expression()
            self.advance()

            return expr

        elif self.isToken(['NUMBER']):
            self.advance()
            return Num(tok["token"])

        elif self.isToken(['COMMAND']):
            expr = self.current["token"]
            self.advance()
            expr = expr[1: -1]
            return Command(expr)
        
        else:
            raise Exception("Invalid basic token.")