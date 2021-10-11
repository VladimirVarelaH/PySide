import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtCore import Qt
from helpers import absPath
from ui_tabla import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # nos conectamos a la base de datos
        conexion = QSqlDatabase.addDatabase("QSQLITE")
        conexion.setDatabaseName(absPath("contactos.db"))
        if not conexion.open():
            print("No se puede conectar a la base de datos")
            sys.exit(True)

        # creamos el modelo
        self.modelo = QSqlTableModel()
        self.modelo.setTable("contactos")
        self.modelo.select()
        self.modelo.setHeaderData(0, Qt.Horizontal, "Id")
        self.modelo.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.modelo.setHeaderData(2, Qt.Horizontal, "Empleo")
        self.modelo.setHeaderData(3, Qt.Horizontal, "Email")

        # configuramos la tabla
        self.tabla.setModel(self.modelo)
        self.tabla.resizeColumnsToContents()
        self.tabla.setColumnHidden(0, True)

        #Se desactiva la edición de los contenidos de la tabla directamente desde la misma
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #Se modifica el modo de seleccion para impedir la selección múltiple
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        #Se setea el modo de selección en selección de fila
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.fila = 1

        #Se recupera la data de la fila seleccionada
        self.tabla.selectionModel().selectionChanged.connect(self.recuperarData)
        #Se conecta la funcion modifyRow
        self.boton_modificar.clicked.connect(self.modifyRow)
        self.boton_nuevo.clicked.connect(self.crateRow)
        self.boton_borrar.clicked.connect(self.deleteRow)


    def recuperarData(self, selection):
        #se verifica que la tabla tenga contenido
        if selection.indexes():
            #Se obtiene el numero de indice de la fila en la que esta haciendo click el usuario
            self.fila = selection.indexes()[0].row()
            #Se recuperan los valores de los datos desde el modelo
            nombre = self.modelo.index(self.fila, 1).data()
            empleo = self.modelo.index(self.fila, 2).data()
            email = self.modelo.index(self.fila, 3).data()
            #se actualizan los campos de texto con la informacion recogida
            self.line_nombre.setText(nombre)
            self.line_empleo.setText(empleo)
            self.line_email.setText(email)

    def modifyRow(self):
        nombre = self.line_nombre.text()
        empleo = self.line_empleo.text()
        email = self.line_email.text()
        if len(nombre)>0 and len(empleo)>0 and len(email)>0:
            #Se introdiuce la nueva data en la DB a traves del modelo
            self.modelo.setData(self.modelo.index(self.fila, 1), nombre)
            self.modelo.setData(self.modelo.index(self.fila, 2), empleo)
            self.modelo.setData(self.modelo.index(self.fila, 3), email)
            #Se confirman los cambios en la DB
            self.modelo.submit()

    def crateRow(self):
        nombre = self.line_nombre.text()
        empleo = self.line_empleo.text()
        email = self.line_email.text()

        if len(nombre)>0 and len(empleo)>0 and len(email)>0:
            nueva_fila = self.modelo.rowCount()
            self.modelo.insertRow(nueva_fila)

            #Se introdiuce la nueva data en la DB a traves del modelo
            self.modelo.setData(self.modelo.index(nueva_fila, 1), nombre)
            self.modelo.setData(self.modelo.index(nueva_fila, 2), empleo)
            self.modelo.setData(self.modelo.index(nueva_fila, 3), email)
            #Se confirman los cambios en la DB
            self.modelo.submit()

            #Se reinician los valores de los campos de texto
            self.line_nombre.setText("")
            self.line_empleo.setText("")
            self.line_email.setText("")
            
        else:
            print('Datos inválidos')

    def deleteRow(self):
        #Comprueba que haya una fila seleccionada
        if len(self.line_nombre.text())>0:
            #Se elimina la fila de la DB
            self.modelo.removeRow(self.fila)
            self.modelo.select()

            #Se reinician los valores de los campos de texto
            self.line_nombre.setText("")
            self.line_empleo.setText("")
            self.line_email.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
