import dominate
from dominate.tags import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Board(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.doc = self.new_doc()
        self.rewrite()
        self.setHtml(str(self.doc))

    def new_doc(self):
        doc = dominate.document()
        with doc.head:
            script(src="https://polyfill.io/v3/polyfill.min.js?features=es6")
            script(type="text/javascript", id="MathJax-script",src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")
            link(rel="stylesheet", href="https://www.w3schools.com/w3css/4/w3.css")
            style(".MathJax {font-size: 1.5em !important;}")
        return doc

    def rewrite(self, data=[]):
        self.doc = self.new_doc()
        with self.doc:
            self.commands()
            self.variables()
            self.parameters()
            if len(data)> 0:
                self.expressions(data[0])
                if len(data) > 1:
                    for i in range(1,len(data)):
                        self.derivations(i, data[i])
        self.setHtml(str(self.doc))

    @div(h3("Parameters:"))
    def parameters(self):
        p("$$None$$", align="center")

    @div(h3("Variables:"))
    def variables(self):
        p("$$x$$", align="center")

    @div(h3("Commands:"))
    def commands(self):
        h5("Domain:")
        p("$$(-10,10)$$", align="center")

    @div(h3("Expressions:"))
    def expressions(self, exprs):
        for expr in exprs:
            p(expr.expr.print("mathjax2"), align="center")

    @div
    def derivations(self, n, diffs):
        h3(f"Derivative of {n}-th order")
        for diff in diffs:
            p(diff.expr.print("mathjax2"), align="center")

