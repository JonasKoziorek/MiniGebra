class Preprocessor:

    def __init__(self, input):
        self.input = input

    def preprocess(self):
        exprs = self.split_to_exprs()
        commands = list(filter(self.check_for_commands, exprs))
        exprs = list(filter(lambda x: x not in commands, exprs))
        return commands, exprs

    def split_to_exprs(self):
        # different expressions are separated by character ;
        lst = [string.strip() for string in self.input.split(";")]
        return list(filter(lambda x: bool(x), lst))

    def check_for_commands(self, expr):
        if expr[0] == '"' and expr[-1] == '"':
            return True
        return False