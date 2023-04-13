class Preprocessor:

    def __init__(self):
        pass

    def preprocess(self, expr):
        return expr
        expr = expr.replace("+", " + ")
        expr = expr.replace("-", " - ")
        expr = expr.replace("*", " * ")
        expr = expr.replace("/", " / ")
        expr = expr.replace("^", " ^ ")
        return expr