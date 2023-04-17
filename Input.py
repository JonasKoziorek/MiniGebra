from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

class Input(QWidget):
    parsed_text = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, name):
        super().__init__()
        self._name = name
        layout = QHBoxLayout()
        self.edit = QLineEdit()
        text = QLabel(self._name)
        layout.addWidget(text)
        layout.addWidget(self.edit)
        self.setLayout(layout)

        self.editingFinished(self.compile_input_)

    def editingFinished(self, func) -> None:
        self.edit.editingFinished.connect(func)
    
    def text(self) -> str:
        return self.edit.text()

    def compile_input_(self):
        text =self.text()
        if text:
            # self.parsed_text.emit(*compile_(text))
            pass
        