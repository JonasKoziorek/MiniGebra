class Command:
    name = ""
    # known directives:
    # domain: R->R or R->R^2 or R->R^3 or R^2->R or R^2->R^3
    # vars: comma separated words/letters => x, y, az
    # params: comma separated words/letters => a, b, abd
    def __init__(self, text: str):
        self.text = text

    def simplify(self):
        return self

    def diff(self):
        return self

    def __repr__(self):
        return f"{self.name}: {self.text}"

class Domain(Command):
    name = "domain"
    def __init__(self, text:str):
        super().__init__(text)

class Vars(Command):
    name = "vars"
    def __init__(self, text:str):
        super().__init__(text)

class Params(Command):
    name = "params"
    def __init__(self, text:str):
        super().__init__(text)

valid_commands = [Domain, Vars, Params]
valid_names = [i.name for i in valid_commands]