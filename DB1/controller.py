import sys
from helpers import absPath
from PySide6.QtSql import QSqlDatabase, QSqlQuery

#Se establece la conección con la base de datos SQLite, que viene con el programa
conection = QSqlDatabase.addDatabase("QSQLITE")
#Se nombra la base de datos a utilizar
conection.setDatabaseName(absPath("contactos.db"))

if not conection.open():
    print('ERROR 500\nno DataBase conection')
    sys.exit(True)
# Cree una consulta y ejecútela de inmediato usando .exec ()
consulta = QSqlQuery()
consulta.exec("DROP TABLE IF EXISTS contactos")
consulta.exec("""
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        nombre VARCHAR(40) NOT NULL,
        empleo VARCHAR(50),
        email VARCHAR(40) NOT NULL
    )""")

#Introducir un solo valor
nombre, empleo, email = "Vladimir", "Desarrollador", "algo@example.com"
consulta.exec(f"""
    INSERT INTO contactos (nombre, empleo, email)
    VALUES ('{nombre}', '{empleo}', '{email})
"""
)

#Introducir varios valores
contactos = [
    ("Manuel", "Desarrollador Web", "manuel@ejemplo.com"),
    ("Lorena", "Gestora de proyectos", "lorena@ejemplo.com"),
    ("Javier", "Analista de datos", "javier@ejemplo.com"),
    ("Marta", "Experta en Python", "marta@ejemplo.com")
]
#se prepara la consulta
consulta.prepare("""
    INSERT INTO contactos (nombre, empleo, email)
    VALUES   (?,?,?)
"""
)
#Se utiliza el formato de consulta para introducir la data
for nombre, empleo, email in contactos:
    consulta.addBindValue(nombre)
    consulta.addBindValue(empleo)
    consulta.addBindValue(email)
    consulta.exec()


#Se hace una consulta a la DB y se almacena el resultado en el objeto consulta
consulta.exec("SELECT nombre, empleo, email FROM contactos")
#Mientras hayan elementos de la consulta se imprimirán en consola
while consulta.next():
    print(
        consulta.value('nombre'),
        consulta.value('empleo'),
        consulta.value('email')
    )

conection.close()
print('\nConexión cerrada? ', not conection.isOpen())