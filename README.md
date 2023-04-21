## MiniGebra
Small clone of GeoGebra. Work In Progress.
![plot](/images/logo.png)

## Aim of the project
This clone will consist of simple graphical user interface for plotting mathematical functions. This project was created for class Scientific calculations in Python at VSB-TUO (information about the class can be currently seen here: https://www.vsb.cz/e-vyuka/en/subject/470-2701/02).


# Implemented features

* parsing of mathematical expressions
* simplification of mathematical expressions
* symbolic differentiation
* plotting of expressions/functions
* saving figures
* GUI

![plot](/images/screenshot.png)

Since I have no time to continue this project, it is halted for now. Current version contains bugs and unfinished work.

# Features that might be implemented in future

* plotting options
* ODE support
* systems of ODEs
* slope fields
* functions of two variables
* complex funtions
* parameters and their animations

# Current project structure

    ├── minigebra
    │   ├── __init__.py
    │   ├── gui
    │   │   ├── __init__.py
    │   │   ├── board.py
    │   │   ├── canvas.py
    │   │   ├── input.py
    │   │   ├── main_window.py
    │   │   └── sidebar.py
    │   ├── interpreter
    │   │   ├── __init__.py
    │   │   ├── atoms
    │   │   │   ├── __init__.py
    │   │   │   ├── atoms.py
    │   │   │   ├── differentiators.py
    │   │   │   ├── formatters.py
    │   │   │   └── simplifiers.py
    │   │   ├── commands.py
    │   │   ├── database.py
    │   │   ├── interpreter.py
    │   │   ├── parser.py
    │   │   ├── preprocessor.py
    │   │   └── tokenizer.py
    │   └── main.py