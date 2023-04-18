from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

class TextEdit(QTextEdit):
    edit_finished = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.textChanged.connect(self.on_text_changed)

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.editingFinished)

    def on_text_changed(self):
        self.timer.start()

    def editingFinished(self):
        self.timer.stop()
        self.edit_finished.emit(self.toPlainText())

class Input(QWidget):

    def __init__(self, name):
        super().__init__()
        self._name = name
        layout = QVBoxLayout()
        self.edit = TextEdit()

        text = QLabel(self._name)
        layout.addWidget(text)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def text(self) -> str:
        return self.edit.toPlainText()

    def editingFinished(self, func):
        self.edit.edit_finished.connect(func)
