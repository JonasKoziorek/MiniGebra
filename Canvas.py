from PyQt5.QtWidgets import QVBoxLayout, QWidget
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import ndarray
import cv2 as cv
import numpy as np

class Canvas(QWidget):
    def __init__(self, image: ndarray = None, parent=None, width:int =5, height:int =5, dpi:int =200, toolbar = True):
        super().__init__()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_position([0,0,1,1])
        self.axes.axis("off")

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, None)

        layout = QVBoxLayout()
        if toolbar:
            layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, x, y):
        self.canvas_setup()
        self.axes.plot(x, y)
        self.canvas.draw()

    def spines(self):
        self.axes.spines['left'].set_position(('axes',0))
        self.axes.spines['bottom'].set_position(('axes',0))
        
        # self.axes.spines['right'].set_position(('axes',0.5))
        # self.axes.spines['top'].set_position(('axes', 0.5))
        
        self.axes.xaxis.set_ticks_position('bottom')
        self.axes.yaxis.set_ticks_position('left')

    def canvas_setup(self):
        self.axes.cla()
        self.axes.hlines(0,-100,100,colors = 'dimgrey')
        self.axes.vlines(0,-100,100,colors = 'dimgrey')
        self.axes.set_xlim(left=-10, right=10)
        self.axes.set_ylim(bottom=-10, top=10)
        self.axes.grid(True)
        self.spines()
