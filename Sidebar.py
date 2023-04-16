from PyQt5.QtWidgets import *
from Input import Input
from Canvas import Canvas

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.input = Input("Enter expression:")
        self.canvas = Canvas(toolbar=False)

        layout = QVBoxLayout()
        layout.addWidget(self.input, 5)
        layout.addWidget(self.canvas, 20)
        self.setLayout(layout)
