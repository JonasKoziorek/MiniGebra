import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
colors = plt.rcParams["axes.prop_cycle"]()
plt.rcParams["figure.autolayout"] = True

from PyQt5.QtWidgets import QVBoxLayout, QWidget

import numpy as np

class PlotData:
    """
    This data type stores information about an expression to be plotted.
    """
    def __init__(self, expr, vars: list[str] = ["x"], domain: tuple[int] = (-10,10), precision:float = 0.01) -> None:
        self.expr = expr # Atom like expr
        self.domain = domain
        self.precision = precision
        self.vars = vars

    def generate(self) -> tuple[np.ndarray]:
        """
        Generates data for plotting.
        """
        a,b = self.domain
        num = int(np.abs(b-a)/self.precision)
        x = np.linspace(a,b,num)
        y = np.array([self.expr({self.vars[0]:i}) for i in x])
        return x,y

class Canvas(QWidget):
    """
    This class represents a canvas where plots are plotted.
    """
    def __init__(self) -> None:
        super().__init__()
        self.fig = Figure(dpi=50)
        self.create_grid_axes()
        self.clear_axes()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, None)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def create_grid_axes(self, rows:int = 1, cols:int = 1) -> None:
        """
        Creates new grid of plots that will be place onto canvas.
        """
        axes = self.fig.subplots(int(rows), int(cols))
        if rows == cols == 1:
            self.axes = np.array([axes]).reshape(1,1)
        else:
            self.axes = axes

    def clear_axes(self) -> None:
        """
        Removes the contents of the plotting slots in the grid.
        """
        [axis.clear() for axis in self.axes.flatten()]
        [axis.axis("off") for axis in self.axes.flatten()]

    def reset_axes(self) -> None:
        """
        Removes plotting slots from the grid.
        """
        [self.fig.delaxes(ax) for ax in self.axes.flatten()]

    def new_grid(self, rows=1, cols=1) -> None:
        """
        Partitions canvas into a grid of new dimensions (rows, cols).
        """
        self.reset_axes()
        self.create_grid_axes(rows, cols)
        self.set_style()

    def set_style(self) -> None:
        """
        Specifies the style of the plots that are shown in the canvas.
        """
        for axis in self.axes.flatten():
            axis.clear()
            axis.hlines(0,-100,100,colors = 'dimgrey')
            axis.vlines(0,-100,100,colors = 'dimgrey')
            axis.set_xlim(left=-10, right=10)
            axis.set_ylim(bottom=-10, top=10)
            axis.grid(True)
            axis.spines['left'].set_position(('axes',0))
            axis.spines['bottom'].set_position(('axes',0))
            axis.xaxis.set_ticks_position('bottom')
            axis.yaxis.set_ticks_position('left')

    def compute_grid_size(self, image_count: int) -> tuple[int]:
        """
        Computes ideal dimensions for the grid of plots.
        """
        factor = np.ceil(np.sqrt(image_count))
        i = -1
        while factor**2 - factor*(i+1) - image_count >= 0:
            i+=1
        return (factor-i,factor)

    def montage(self, datasets: list[list[PlotData]]) -> None:
        """
        Displays several plots on the plotting canvas.
        """
        datasets = [item for sub_list in datasets for item in sub_list]
        if len(datasets) > 0:
            x, y  = self.compute_grid_size(len(datasets))
            self.new_grid(x,y)
            for i, axis in enumerate(self.axes.flatten()):
                try:
                    x,y = datasets[i].generate()
                    c = next(colors)["color"]
                    axis.plot(x,y, linewidth = 5, color = c)
                    axis.set_title(datasets[i].expr.print("mathjax1"), fontsize=30)
                except IndexError:
                    axis.clear()
                    axis.axis("off")
            self.canvas.draw()
