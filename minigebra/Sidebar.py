from PyQt5.QtWidgets import *
from Input import Input
from Board import Board
from Slider import Slider

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.input = Input("Enter expression:")
        self.board = Board()
        self.slider = Slider("x")
        self.slider.changeCount(20)
        self.slider.changeRange([-10,10])
        self.slider.recalcValue()

        layout = QVBoxLayout()
        layout.addWidget(self.input, 5)
        layout.addWidget(self.slider, 5)
        layout.addWidget(self.board, 20)
        self.setLayout(layout)
