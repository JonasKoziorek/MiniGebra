from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

class Input(QWidget):
    parsed_text = pyqtSignal(list)

    def __init__(self, name):
        super().__init__()
        self._name = name
        layout = QHBoxLayout()
        self.edit = QLineEdit()
        text = QLabel(self._name)
        layout.addWidget(text)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def editingFinished(self, func) -> None:
        self.edit.editingFinished.connect(func)
    
    def text(self) -> str:
        return self.edit.text()
