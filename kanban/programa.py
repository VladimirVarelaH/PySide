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
            i.itemDoubleClicked.connect(self.updateTaskState)
        
        if existsFile(absPath("tareas.csv")):
            with open(absPath("tareas.csv"), newline="\n") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for lista, nombre in reader:
                    item = QListWidgetItem(nombre)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.listas[int(lista)].addItem(item)


    def eventFilter(self, source, event):
        if (event.type() == QEvent.ContextMenu):
            item = source.itemAt(event.pos())
            # creamos un menu conextual sobre el item
            menu = QMenu()
            #Se crean las opciones del menu con sus funciones
            menu.addAction("Testing", lambda: self.testing(item))
            menu.addAction("Añadir Tarea", self.addTask)
            menu.addAction("Eliminar Tarea", lambda: self.deleteTask(item))
            menu.addAction("Avanzar Estado", lambda: self.updateTaskState(item))
            menu.addAction("Revobinar Estado", lambda: self.reverseTaskState(item))

            if menu.exec(event.globalPos()):
                return True

        #Si no detectla el evento solicitado, ejecuta como si nada
        return super().eventFilter(source, event)



    #_____ METHODS ________#

    def testing(self, item): 
        #Comprueba si el item señeccionado es un elemento de la lista
        if type(item) == QListWidgetItem:
            print(item.text())
    
    def addTask(self):
        tarea, _ = QInputDialog().getText(self, "Tareas", "¿Nombre de la tarea")
        if tarea:
            item = QListWidgetItem(tarea)
            item.setTextAlignment(Qt.AlignCenter)
            self.lista_Pendientes.addItem(item)

    def deleteTask(self, item):
        #Comprueba si el item señeccionado es un elemento de la lista
        if type(item) == QListWidgetItem:
            index = item.listWidget().row(item)
            item.listWidget().takeItem(index)
            print("eliminando",item.text(), "de la fila", index)

    def updateTaskState(self, item):
        #Comprueba si el item señeccionado es un elemento de la lista
        if type(item) == QListWidgetItem:
            #se obtiene la lista contenedora
            lista = item.listWidget()
            index = lista.row(item)
            #Se elimina la tarea de la lista actual
            lista.takeItem(index)

            if lista == self.lista_Pendientes:
                self.lista_EnProgreso.addItem(item)
            elif lista == self.lista_EnProgreso:
                self.lista_Completadas.addItem(item)

    def reverseTaskState(self, item):
        #Comprueba si el item señeccionado es un elemento de la lista
        if type(item) == QListWidgetItem:
            #se obtiene la lista contenedora
            lista = item.listWidget()
            index = lista.row(item)

            if lista == self.lista_EnProgreso:
                #Se elimina la tarea de la lista actual
                lista.takeItem(index)
                self.lista_Pendientes.addItem(item)
            elif lista == self.lista_Completadas:
                lista.takeItem(index)
                self.lista_EnProgreso.addItem(item)

    def closeEvent(self, event):
        tareas = []
        for i, lista in enumerate(self.listas):
            for j in range(lista.count()):
                tareas.append([i, lista.item(j).text()])
                print(tareas)
        with open(absPath("tareas.csv"), "w") as CSVfile:
            writer = csv.writer(CSVfile, delimiter=",")
            
            writer.writerows(tareas)
        
        event.accept()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
