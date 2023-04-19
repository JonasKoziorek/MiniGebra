from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
import numpy as np
from numpy import ndarray

class SliderData:
    """
    Poskytuje datovou strukturu, která posuvníku :class:`~ExamineWindow.Slider` dává způsob jak exportovat svůj stav.
    """    

    def __init__(self, min: int=-1, max: int=-1, curVal: int=-1, count: int=-1):
        self.min = min
        self.max = max
        self.curVal = curVal
        self.count = count
        self.checked = 0

    def getRange(self) -> ndarray:
        """
        Rozseká interval od :attr:`ExamineWindow.SliderData.min` do :attr:`ExamineWindow.SliderData.max` na :attr:`ExamineWindow.SliderData.count` částí.
        
        :return: rozsekaný interval
        :rtype: ndarray
        """    
        return np.linspace(self.min, self.max, self.count)


class Slider(QWidget):
    """
    Tato třída reprezentuje posuvník, používaný v celku :class:`~ExamineWindow.SliderInputUnit.SliderInputUnit`.

    .. figure:: figures/obrazovka\ (25).png
        :align: center

        Zde je vidět posuvník typu  :class:`~ExamineWindow.Slider.Slider` používaný v celku :class:`~ExamineWindow.SliderInputUnit.SliderInputUnit`.

    """
    valueChanged = pyqtSignal(float)
    """
    Tento signál je vyslán pokaždé, když se hodnota posuvníku změní. Typem tohoto signálu je float.
    """

    def __init__(self, text: str):
        super().__init__()
        #params
        self.__text = text
        self.__linspaceArr = []

        #widgets
        self.slider = self.__createSlider()
        self.label = self.__createLabel()

        #layout
        self.setLayout(self.__createLayout())

    def changeCount(self, count: int) -> None:
        """
        Změní rozmezí posuvníku na celočíselný iterval [0, count-1].

        :param count: horní mez intervalu posuvníku
        :type count: int
        """        
        self.slider.setRange(0, count-1)

    def changeRange(self, range: list) -> None:
        """
        Nastaví hodnoty posuvníku na celočíselný interval od *range[0]* do *range[1]*.

        :param range: dvouprvkový seznam čísel
        """
        upperBound = self.slider.maximum()+1
        self.__linspaceArr = np.linspace(range[0], range[1], upperBound)
        lowerBound = self.slider.minimum()
        self.slider.setValue(lowerBound)

    def changeText(self, text: str) -> None:
        """
        Nastaví hodnotu atributu :attr:`Slider.__text` na *text*.
        """
        self.__text = text

    def recalcValue(self) -> None:
        """
        Nastaví hodnotu posuvníku na výchozí hodnotu / hodnotu, která je nejvíce vlevo.
        """
        self.slider.setValue(self.slider.minimum())
        self.label.setText(f"{self.__text}: {self.__linspaceArr[0]}")

    def getStatus(self) -> SliderData:
        """
        Stav posuvníku lze popsat pomocí typu :class:`~ExamineWindow.Slider.SliderData`.
        Tato funkce na výstup vrací stav této třídy popsaný právě tímto datovým typem.
        """
        min = self.__linspaceArr[0]
        max = self.__linspaceArr[-1]
        curVal = self.__linspaceArr[self.slider.value()]
        count = self.slider.maximum()+1
        return SliderData(min, max ,curVal, count)

    def __changeValue(self, value):
        self.label.setText(f"{self.__text}: {round(self.__linspaceArr[value], 4)}")

    def __createSlider(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setTracking(True)
        slider.setRange(0,0)
        slider.setPageStep(1)
        slider.valueChanged.connect(self.__changeValue)
        slider.valueChanged.connect(self.__valueChanged)
        return slider

    def __createLabel(self):
        label = QLabel(f"{self.__text}: {self.slider.value()}", self)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setMinimumWidth(140)
        return label

    def __createLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addSpacing(15)
        layout.addWidget(self.slider)
        return layout

    def __valueChanged(self, value: int):
        self.valueChanged.emit(self.__linspaceArr[value])

