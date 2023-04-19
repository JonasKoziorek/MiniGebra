import Atoms

# important data used by many sub parts of the program will be held here
class Database:
    built_in_functions = Atoms.built_in_functions
    def __init__(self):
        self.expressions = []
        self.variables = []
        self.parameters = []
