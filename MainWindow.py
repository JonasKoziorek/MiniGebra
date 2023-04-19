from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Canvas import Canvas 
from Sidebar import Sidebar
import cv2 as cv
from Interpreter import Interpreter

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MiniGebra")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(0,0, 500, 500)
        self.showMaximized()

        self.canvas = Canvas()
        self.sidebar = Sidebar()
        self.interpreter = Interpreter()
        self.sidebar.input.editingFinished(self.invoke_plot)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 5)
        layout.addWidget(self.canvas, 20)
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def invoke_plot(self, text: str) -> None:
        if text == "":
            self.canvas.reset_axes()
            self.canvas.create_grid_axes()
            self.canvas.clear_axes()
            self.canvas.canvas.draw()
        elif text:
            try:
                commands, data = self.interpreter.interpret_text(text, diff_order=1)
                self.canvas.montage(data)
                self.sidebar.board.rewrite(data)
            except Exception as e:
                print(e)
