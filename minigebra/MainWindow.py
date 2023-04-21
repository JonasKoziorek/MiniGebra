from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Canvas import Canvas 
from Sidebar import Sidebar
from Interpreter import Interpreter
from Database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MiniGebra")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(0,0, 500, 500)
        self.showMaximized()

        self.canvas = Canvas()
        self.sidebar = Sidebar()
        self.database = Database()
        self.interpreter = Interpreter(self.database)
        self.sidebar.input.editingFinished(self.process_input)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 5)
        layout.addWidget(self.canvas, 20)
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def process_input(self, text: str) -> None:
        if text == "":
            self.canvas.reset_axes()
            self.canvas.create_grid_axes()
            self.canvas.clear_axes()
            self.canvas.canvas.draw()
        elif text:
            try:
                self.interpreter.interpret_text(text)
                self.interpreter.generate_data()
                self.canvas.montage(self.database.plot_data)
                self.sidebar.board.rewrite(self.database)
            except Exception as e:
                print(e)
