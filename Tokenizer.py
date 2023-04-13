import re

# the regex patterns specify substring in the beginning of a string with matching pattern
tokens = [
    [r"^\s+", 'WHITESPACE'], # selects whitespace, tabs, newlines at the beginning of a string
    [r"^-?\d+(?:\.\d+)?", 'NUMBER'], # selects numbers at the beginning of a string including floats and negative numbers
    [r"^[a-zA-Z]+", 'IDENT'], # selects variables specified as characters or words consisting of letters
    [r'^"[^"]+"', 'STRING'], # selects strings denoted by "string", only double quotes
    [r"^\+", 'PLUS'], # selects plus sign
    [r"^-", 'MINUS'], # selects minus sign
    [r"^\*", 'MUL'], # selects multiplication sign
    [r"^\^", 'EXP'], # selects exponentation sign
    [r"^\/", 'DIV'], # selects division sign
    [r"^\(", 'LPAR'], # selects left paranthesis sign
    [r"^\)", 'RPAR'], # selects right paranthesis sign
    [r"^,", 'COMMA'], # selects comma
]
tokens = [(re.compile(i), j) for i,j in tokens]

class Tokenizer:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.cursor = -1
        self.string = None

    def read(self, string: str) -> None:
        self.cursor = 0
        self.string = string

    def next_match(self) -> dict:
        if self.cursor != len(self.string):
            text = self.string[self.cursor:]
            for (pattern, type) in self.tokens:
                match = pattern.match(text)
                if match:
                    self.cursor += len(match[0])
                    if type == 'WHITESPACE':
                        return self.next_match()
                    else:
                        return {"token": match[0], "type": type}
            return {"token": None, "type": "INVALID_CHAR"}

