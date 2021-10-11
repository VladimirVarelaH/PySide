from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QListWidgetItem, QInputDialog)
from PySide6.QtCore import Qt, QEvent
from ui_kanban import Ui_MainWindow
from helpers import *
import csv


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Se almacenan las listas en una lista de listas
        self.listas = [self.lista_Pendientes, self.lista_EnProgreso, self.lista_Completadas]
        #Se recorren las listas limpiando su contenido
        for i in self.listas:
            i.clear()
            i.installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.ContextMenu):
            # creamos un menu conextual sobre el item
            menu = QMenu()
            menu.addAction("Añadir tarea", self.testing)
            if menu.exec(event.globalPos()):
                return True
        return super().eventFilter(source, event)

    def testing(self): 
        print('testing')


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
