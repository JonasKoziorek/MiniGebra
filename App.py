from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
from MainWindow import MainWindow
from Atoms import built_in_functions
from Interpreter import Interpreter

# tohle je potreba aby se mi spravne ukazovaly errory
# -----
sys._excepthook = sys.excepthook
def __my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = __my_exception_hook
# -----

if __name__ == '__main__':
    type = "GUI"
    # type = "CLI"
    if type == "GUI":
        app = QApplication(sys.argv)
        # show available font families
        # print(QFontDatabase().families())
        font = QFont("Arimo for Powerline", 10)
        app.setFont(font)
        w = MainWindow()
        sys.exit(app.exec_())

    elif type == "CLI":
        I = Interpreter(built_in_functions)
        I.interpreter_loop(plot=True, diff_order=1, padding=2)

    else:
        raise Exception(f"You selected an app option {type}. This option is not supported.")

        