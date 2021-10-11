import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import Qt
from helpers import absPath
from ui_tabla import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Se extraen los datos del archivo contactos.json
        with open(absPath(r'./contactos.json'), "r") as fichero:
            self.datos = json.load(fichero)
            self.keys = list(self.datos[0].keys())

        #Se configura la cantidad de filas y columnas segun la informacion cargada
        self.tabla.setRowCount(len(self.datos))
        self.tabla.setColumnCount(len(self.keys))
        #Se configuran las cabeceras de las filas y columnas
        self.tabla.setHorizontalHeaderLabels(self.keys)

        #Se recorre la data, dándole el valor correspondiente a cada celda
        for i, fila in enumerate(self.datos):
            for j, columna in enumerate(self.keys):
                item = QTableWidgetItem()
                item.setData(Qt.EditRole, fila[columna])
                self.tabla.setItem(i, j, item)
        #Se adapta el tamaño de la columa al contenido
        self.tabla.resizeColumnsToContents()

        #Se le da formato capitalize a las cabeceras de cada columna
        count = 0
        for i in self.keys:
            self.tabla.setHorizontalHeaderItem(count, QTableWidgetItem(i.capitalize()))
            count +=1

        #Se recuperan los valores modificados por el usuario
        self.tabla.itemChanged.connect(self.getNewValue)

    def getNewValue(self, item):
        fila, columna = item.row(), self.keys[item.column()]
        self.datos[fila][columna] = item.data(Qt.EditRole)
        with open(absPath(r'./contactos.json'), "w") as fichero:
            json.dump(self.datos, fichero)

        with open(absPath(r'./contactos.json'), "r") as fichero:
            self.datos = json.load(fichero)
            self.keys = list(self.datos[0].keys())
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
