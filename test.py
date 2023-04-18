from PyQt5.QtWebEngineWidgets import QWebEngineView

class LatexWidget(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setHtml("""
            <html>
                <head>
                    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                    <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
                </head>
                <body>
                    <div id="latex"></div>
                </body>
            </html>
        """)
        
    def setLatex(self, latex):
        self.setHtml("""
            <html>
                <head>
                    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                    <script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
                </head>
                <body>
                    <div id="latex">%s</div>
                </body>
            </html>
        """ % latex)
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.latex_widget = LatexWidget()
        layout.addWidget(self.latex_widget)

        self.setLayout(layout)

        self.setWindowTitle('Latex Widget')
        self.setWindowIcon(QIcon('icon.png'))
        self.resize(400, 300)
        self.show()

        self.latex_widget.setLatex(r'Some latex $$(\phi \times \epsilon \in \{1,2,3\})$$')


app = QApplication(sys.argv)
w = App()
sys.exit(app.exec_())