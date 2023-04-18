from PyQt5.QtWidgets import *
from Canvas import Canvas 
from Sidebar import Sidebar
import cv2 as cv
from Interpreter import Interpreter
from Atoms import built_in_functions

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0,0, 500, 500)
        self.showMaximized()

        self.canvas = Canvas()
        self.sidebar = Sidebar()
        self.interpreter = Interpreter(built_in_functions)
        self.sidebar.input.editingFinished(self.invoke_plot)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 5)
        layout.addWidget(self.canvas, 20)
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def invoke_plot(self, text):
        if text:
            try:
                data = self.interpreter.interpret_text(text, diff_order=1)
                self.canvas.montage(data)
                self.sidebar.board.rewrite(data)
            except:
                pass
