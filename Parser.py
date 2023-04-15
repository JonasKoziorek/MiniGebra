from Atoms import Mul, Expon, Div, Plus, Minus, Variable, Function, Number
from Commands import valid_names, valid_commands, Command
from Errors import ParseError

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current = []

    def parse_expr(self, string):
        self.tokenizer.read(string)
        self.current = self.tokenizer.next_match()
        try:
            return self.expression()
        except Exception as e:
            raise ParseError(f"Following error occured while parsing: {e}")

    def parse_command(self, command):
        command = command[1:-1]
        tokens = command.split(":")
        if len(tokens) == 2:
            name = tokens[0]
            body = tokens[1]
            if name in valid_names:
                ind = valid_names.index(name)
                type_ = valid_commands[ind]
                return type_(body)
            else:
                raise Exception(f"Unknown command {command}.\nAvailable commands are {valid_names}")
        else:
            raise ParseError(f"Command {command} is not valid.")
    


    def isValid(self, tokens: list[str]):
        if self.current["type"] == "INVALID_CHAR":
            # raise Exception("This character is not supported.")
            return False

        if self.isToken(tokens) == False:
            # raise Exception("Incorrect token encountered.")
            return False
        
        return True

    def advance(self):
        self.current = self.tokenizer.next_match()

    def isToken(self, tokens):
        if self.current:
            return self.current["type"] in tokens

    def expression(self):
        return self.addition()

    def addition(self):
        left = self.multiplication()

        while self.isToken(['PLUS', 'MINUS']):
            type = self.current["type"]
            self.advance()
            if type == "PLUS":
                left = Plus(left, self.multiplication())
            elif type == "MINUS":
                left = Minus(left, self.multiplication())

        return left

    def function(self):
        pass

    def multiplication(self):
        left = self.exponentiation()

        while self.isToken(['MUL', 'DIV']):
            type = self.current["type"]
            self.advance()
            if type == "MUL":
                left = Mul(left, self.exponentiation())
            elif type == "DIV":
                left = Div(left, self.exponentiation())

        return left

    def exponentiation(self):
        left = self.basic()

        while self.isToken(['EXP']):
            self.advance()
            left = Expon(left, self.basic())

        return left

    def function(self):
        left = self.multiplication()

        if self.isToken(['LPAR']):
            self.advance()
            args = [self.expression()]

            while self.isToken(['COMMA']):
                self.advance()
                args.append(self.expression())

            self.advance()
            if type(left) == Variable:
                return Function(left.value, args )
            else:
                raise Exception("Incorret function expression.")
        else:
            return left

    def basic(self):
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
                name = Variable(tok["token"]).value
                return Function(name, args )
            
            else:
                return Variable(tok["token"])

        elif self.isToken(['LPAR']):
            self.advance()
            expr = self.expression()
            self.advance()

            return expr

        elif self.isToken(['NUMBER']):
            self.advance()
            return Number(tok["token"])

        elif self.isToken(['COMMAND']):
            expr = self.current["token"]
            self.advance()
            expr = expr[1: -1]
            return Command(expr)
            # return  Parser(Tokenizer(tokens)).read(expr)
        
        else:
            raise Exception("Invalid basic token.")