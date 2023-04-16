from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
from MainWindow import MainWindow

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
    app = QApplication(sys.argv)
    # show available font families
    # print(QFontDatabase().families())
    font = QFont("Arimo for Powerline", 10)
    app.setFont(font)
    w = MainWindow()
    sys.exit(app.exec_())