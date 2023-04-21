from .atoms import BUILT_IN_FUNCTIONS

# important data used by many sub parts of the program will be held here
class Database:
    built_in_functions = BUILT_IN_FUNCTIONS
    def __init__(self):
        self.expressions = []
        self.variables = ["x"]
        self.parameters = ["a"]
        self.domain = (-10,10)
        self.diff_order = 1
        self.precision = 0.01
        self.plot_data = []
