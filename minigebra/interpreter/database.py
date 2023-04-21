from .atoms import BUILT_IN_FUNCTIONS

# for type hints
from ..gui.canvas import PlotData
from .atoms import Atom, Function

class Database:
    """
    This class is a container for metadata which is used across the program.
    """
    built_in_functions: list[Function] = BUILT_IN_FUNCTIONS
    def __init__(self):
        self.expressions: list[list[Atom]] = []
        self.variables: list[str] = ["x"]
        self.parameters: list[str] = ["a"]
        self.domain: tuple[int] = (-10,10)
        self.diff_order: int = 1
        self.precision: float = 0.01
        self.plot_data: list[list[PlotData]] = []
