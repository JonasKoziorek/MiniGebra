class Preprocessor:

    def __init__(self, input):
        self.input = input

    def preprocess(self):
        exprs = self.split_to_exprs()
        commands = list(filter(self.check_for_commands, exprs))
        exprs = list(filter(lambda x: x not in commands, exprs))
        return commands, exprs

        return self.split_to_exprs()
        # expr = expr.replace("+", " + ")
        # expr = expr.replace("-", " - ")
        # expr = expr.replace("*", " * ")
        # expr = expr.replace("/", " / ")
        # expr = expr.replace("^", " ^ ")
        # return expr

    def split_to_exprs(self):
        # different expressions are separated by character ;
        return self.input.split(";")

    def check_for_commands(self, expr):
        if expr[0] == '"' and expr[-1] == '"':
            return True
        return False