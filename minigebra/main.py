from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys

from .gui import MainWindow
from .interpreter import Interpreter


def run(type: str) -> None:
    if type == "GUI":
        app = QApplication(sys.argv)
        font = QFont("Arimo for Powerline", 13)
        app.setFont(font)
        w = MainWindow()
        sys.exit(app.exec_())

    elif type == "CLI":
        I = Interpreter()
        I.interpreter_loop(plot=True, diff_order=1, padding=2)

    else:
        raise Exception(f"You selected an app option {type}. Supported options are GUI and CLI.")
