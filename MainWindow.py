from PyQt5.QtWidgets import *
from Canvas import Canvas 
from Sidebar import Sidebar
import cv2 as cv

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0,0, 500, 500)
        self.showMaximized()

        canvas = Canvas()
        sidebar = Sidebar()
        sidebar.input.parsed_text.connect(canvas.plot)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(sidebar, 5)
        layout.addWidget(canvas, 20)
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()
