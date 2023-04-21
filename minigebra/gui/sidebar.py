from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .input import Input
from .board import Board

class Sidebar(QWidget):
    """
    This widget represents a sidebar where input prompt and latex output board are shown.
    """
    def __init__(self):
        super().__init__()

        self.input = Input("Enter expression:")
        self.board = Board()

        layout = QVBoxLayout()
        layout.addWidget(self.input, 5)
        layout.addWidget(self.board, 20)
        self.setLayout(layout)
