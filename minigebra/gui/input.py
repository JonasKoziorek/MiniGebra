from PyQt5.QtWidgets import QTextEdit, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer

class TextEdit(QTextEdit):
    """
    Represents an input prompt in the gui where expressions and commands can be inputed by user.
    """
    edit_finished = pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

        self.textChanged.connect(self.on_text_changed)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.editingFinished)

    def on_text_changed(self) -> None:
        """
        Starts a timer which knows when user started editing the widget.
        """
        self.timer.start()

    def editingFinished(self) -> None:
        """
        After user stops editing the widget, it sends contents of the widget in string format through a signal.
        """
        self.timer.stop()
        self.edit_finished.emit(self.toPlainText())

class Input(QWidget):
    """
    Represents a widget where user can input expressions and commands. 
    """

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        layout = QVBoxLayout()
        self.edit = TextEdit()

        text = QLabel(self._name)
        layout.addWidget(text)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def text(self) -> str:
        """
        Converts contents of the input prompt to text.
        """
        return self.edit.toPlainText()

    def editingFinished(self, func: callable) -> None:
        """
        When editing of the input prompt is finished, function "func" is called.
        """
        self.edit.edit_finished.connect(func)
