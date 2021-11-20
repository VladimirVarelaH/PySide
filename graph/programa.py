from PySide6 import QtWidgets
from pyqtgraph.graphicsItems.ScatterPlotItem import SymbolAtlas
from ui_monitor import Ui_MainWindow
from functools import partial
import pyqtgraph as pg  # pip install pyqtgraph
import random

"""
"pen":"pg.mkPen('b', wifth=2)",
"pen":"pg.mkPen('r', wifth=2)", 
"""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.vectores = [
            {"name":"Uno", "symbol":"o", "values":[10,11,13,12],"symbolSize":10,  "symbolBrush":"b"},
            {"name":"Dos", "symbol":"o", "values":[1,3,-3,2],"symbolSize":10, "symbolBrush":"r"},
            {"name":"Tres", "symbol":"o", "values":[-1,-3,3,-2],"symbolSize":10, "symbolBrush":"g"}
        ]
        #Se le dan los valores al combo box
        for i in self.vectores:
            self.comboBox.addItem(i['name'])

        self.buildGraph()
        self.pushButton.clicked.connect(self.addData)
        self.pushButton_2.clicked.connect(partial(self.addData, True))

    def buildGraph(self):
        #Se añade una leyenda con el nombre de los vectores
        self.widget.addLegend()
        #Se añade una cuadricula para facilitar la lectura del grafico
        self.widget.showGrid(x=True, y=True)
        # self.widget.setBackground('w')
        self.widget.setTitle('Monitor de Temperaturas')
        self.widget.setYRange(-30, 30)
        self.widget.setLabel('left', 'Temperatura (Cº)')
        self.widget.setLabel('bottom', 'Horario')

        self.graphs = []
        # Se genera la visualizacion de manera dinamica
        for i in self.vectores:
            plot = self.widget.plot(i['values'],**i, pen=pg.mkPen(i['symbolBrush'], width=2))
            self.graphs.append(plot)

    def addData(self, auto=False):
        if not auto:
            #Obtiene la data desde el spinbox y el combobox
            vector = self.comboBox.currentIndex()
            temperature = self.spinBox.value()

            #Almacena la lista de valores del vector a modificar
            my_vector = self.vectores[vector]['values']
            #Añade el nuevo valor
            my_vector.append(temperature)
            #Actualiza el grafico
            self.graphs[vector].setData(my_vector)
        else: 
            for i, vector in enumerate(self.vectores):
                my_vector = vector['values']
                maxi = max(my_vector)+1
                mini = min(my_vector)-1
                temperature = random.randint(mini, maxi)
                #Añade el nuevo valor
                my_vector.append(temperature)
                #Actualiza el grafico
                self.graphs[i].setData(my_vector)



if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()
