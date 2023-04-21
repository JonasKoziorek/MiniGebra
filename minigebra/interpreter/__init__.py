"""
This subpackage provides functionality for interpreting mathematical expressions inputed as plain text.
Supported functionalities include:

* converting math expressions from text to AST/internal representation
* converting internal representation to text or latex format
* simplifying expressions
* differentiating expressions
* evaluating expressions

"""

from .interpreter import Interpreter