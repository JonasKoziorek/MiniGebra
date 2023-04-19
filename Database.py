import Atoms

# important data used by many sub parts of the program will be held here
class Database:
    built_in_functions = Atoms.built_in_functions
    def __init__(self):
        self.expressions = []
        self.variables = ["x"]
        self.parameters = ["a"]
        self.domain = (-10,10)
        self.diff_order = 1
        self.precision = 0.01
        self.plot_data = []
