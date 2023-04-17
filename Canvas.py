from PyQt5.QtWidgets import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import ndarray
import cv2 as cv
import numpy as np

class Canvas(QWidget):
    def __init__(self, image: ndarray = None, parent=None, dpi:int = 50, toolbar = True):
        super().__init__()
        self.dpi = dpi
        self.canvas = FigureCanvasQTAgg()
        self.toolbar = NavigationToolbar(self.canvas, None)

        layout = QVBoxLayout()
        if toolbar:
            layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def create_grid_axes(self, rows:int = 1, cols:int = 1):
        axes = self.fig.subplots(int(rows), int(cols))
        if rows == cols == 1:
            self.axes = np.array([axes])
        else:
            self.axes = axes

    def create_new_fig(self):
        self.fig = Figure(dpi=self.dpi)
        self.canvas.figure = self.fig

    def new_grid(self, rows=1, cols=1):
        self.create_new_fig()
        self.create_grid_axes(rows, cols)
        self.set_style()

    def set_style(self):
        for axis in self.axes.flatten():
            axis.cla()
            axis.hlines(0,-100,100,colors = 'dimgrey')
            axis.vlines(0,-100,100,colors = 'dimgrey')
            axis.set_xlim(left=-10, right=10)
            axis.set_ylim(bottom=-10, top=10)
            axis.grid(True)
            axis.spines['left'].set_position(('axes',0))
            axis.spines['bottom'].set_position(('axes',0))
            axis.xaxis.set_ticks_position('bottom')
            axis.yaxis.set_ticks_position('left')
            axis.axis("off")
            # axis.set_position([0,0,1,1])

    def compute_grid_size(self, image_count: int) -> tuple[int]:
        factor = np.ceil(np.sqrt(image_count))
        i = -1
        while factor**2 - factor*(i+1) - image_count >= 0:
            i+=1
        return (factor-i,factor)

    def montage(self, datasets: list[list], names=[]):
        x, y  = self.compute_grid_size(len(datasets))
        self.new_grid(x,y)
        for i, axis in enumerate(self.axes.flatten()):
            axis.plot(*datasets[i])
        self.refresh()

    def refresh(self):
        self.canvas.draw()
