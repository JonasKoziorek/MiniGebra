from Tokenizer import tokens, Tokenizer
from Atoms import *

###### inspired by article: https://itnext.io/writing-a-mathematical-expression-parser-35b0b78f869e

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current = []

    def read(self, string):
        self.tokenizer.read(string)
        self.current = self.tokenizer.next_match()
        try:
            return self.expression()
        except Exception as e:
            raise Exception(f"Following error occured while parsing: {e}")
    
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
                left = Multiplication(left, self.exponentiation())
            elif type == "DIV":
                left = Division(left, self.exponentiation())

        return left

    def exponentiation(self):
        left = self.basic()

        while self.isToken(['EXP']):
            self.advance()
            left = Exponentiation(left, self.basic())

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

        if self.isToken(["IDENT"]):
            self.advance()
            next = self.current

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


        elif self.isToken(['STRING']):
            expr = self.current["token"]
            self.advance()
            expr = expr[1: -1]
            return  Parser(Tokenizer(tokens)).read(expr)
        
        else:
            raise Exception("Invalid basic token.")


# class Parser:

#     def __init__(self, tokenizer):
#         self.tokenizer = tokenizer
#         self.current = []

#     def read(self, string):
#         self.tokenizer.read(string)
#         self.current = self.tokenizer.next_match()
#         try:
#             return self.expression()
#         except Exception as e:
#             raise Exception(f"Following error occured while parsing: {e}")
    
#     def isValid(self, tokens: list[str]):
#         if self.current["type"] == "INVALID_CHAR":
#             # raise Exception("This character is not supported.")
#             return False

#         if self.isToken(tokens) == False:
#             # raise Exception("Incorrect token encountered.")
#             return False
        
#         return True

#     def advance(self):
#         self.current = self.tokenizer.next_match()

#     def isToken(self, tokens):
#         if self.current:
#             return self.current["type"] in tokens

#     def expression(self):
#         return self.addition()

#     def addition(self):
#         left = self.function()

#         while self.isToken(['PLUS', 'MINUS']):
#             type = self.current["type"]
#             self.advance()
#             if type == "PLUS":
#                 left = Plus(left, self.function())
#             elif type == "MINUS":
#                 left = Minus(left, self.function())

#         return left

#     def call(self):
#         pass

#     def multiplication(self):
#         left = self.exponentiation()

#         while self.isToken(['MUL', 'DIV']):
#             type = self.current["type"]
#             self.advance()
#             if type == "MUL":
#                 left = Multiplication(left, self.exponentiation())
#             elif type == "DIV":
#                 left = Division(left, self.exponentiation())

#         return left

#     def exponentiation(self):
#         left = self.basic()

#         while self.isToken(['EXP']):
#             self.advance()
#             left = Exponentiation(left, self.basic())

#         return left

#     def function(self):
#         possible_func = self.multiplication()

#         # if self.isToken(['NUMBER', 'IDENT']):
#         #     return Function(possible_func.value, [self.function()] )
        
#         if self.isToken(['LPAR']):
#             self.advance()
#             args = [self.expression()]

#             while self.isToken(['COMMA']):
#                 self.advance()
#                 args.append(self.expression())

#             self.advance()
#             if type(possible_func) == Variable:
#                 return Function(possible_func.value, args )
#             else:
#                 raise Exception("Incorret function expression.")
        
#         else:

#             return possible_func

#     def basic(self):
#         tok = self.current
#         if self.isToken(['LPAR']):
#             self.advance()
#             expr = self.expression()
#             self.advance()

#             return expr

#         elif self.isToken(['NUMBER']):
#             self.advance()
#             return Number(tok["token"])

#         elif self.isToken('IDENT'):
#             self.advance()
#             return Variable(tok["token"])

#         elif self.isToken(['STRING']):
#             expr = self.current["token"]
#             self.advance()
#             expr = expr[1: -1]
#             return  Parser(Tokenizer(tokens)).read(expr)
        
#         else:
#             raise Exception("Invalid basic token.")
