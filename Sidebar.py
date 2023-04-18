from PyQt5.QtWidgets import *
from Input import Input
from Board import Board

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.input = Input("Enter expression:")
        self.board = Board()
        # self.board.setLatex(r'Some latex $$(\phi \times \epsilon \in \{1,2,3\})$$')

        layout = QVBoxLayout()
        layout.addWidget(self.input, 5)
        layout.addWidget(self.board, 20)
        self.setLayout(layout)
