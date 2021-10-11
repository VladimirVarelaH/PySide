import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtCore import Qt
from helpers import absPath
from ui_tabla import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Se establece la conección con la base de datos SQLite, que viene con el programa
        conection = QSqlDatabase.addDatabase("QSQLITE")
        #Se nombra la base de datos a utilizar
        conection.setDatabaseName(absPath("Contactos.db"))

        if not conection.open():
            print('ERROR 500\nno DataBase conection')
            sys.exit(True)
        
        #Se crea un modelo de la tabla contactos en la base de datos
        model = QSqlTableModel()
        model.setTable('contactos')
        model.select()

        model.setHeaderData(0, Qt.Horizontal, "Id")
        model.setHeaderData(1, Qt.Horizontal, "Nombre")
        model.setHeaderData(2, Qt.Horizontal, "Empleo")
        model.setHeaderData(3, Qt.Horizontal, "Correo")

        #Se le pasa el modelo a la tabla de la vista para darle el formato
        self.tabla.setModel(model)
        self.tabla.setColumnHidden(0, True)
        self.tabla.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
