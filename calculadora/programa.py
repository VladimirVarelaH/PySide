from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLCDNumber, QPushButton)
from functools import partial
from helpers import *

"""
hay un problema con el amacenamiento del operador en memoria
"""

#Se crea una clase para extender las propiedades de QLCDNumber
class Calculator(QLCDNumber):
    def __init__(self):
        #Se configura la cantidad de numeros admitidos en pantalla y el estilo de los mismos
        super().__init__(digitCount=12, segmentStyle=QLCDNumber.Flat)
        self.text = ""
        self.operation = ''
        self.memory = 0
        self.operator = 0
        self.special = False

    def write(self, char):
        if(self.special):
            self.display('')
            self.special = False
        #Confirma que sólo haya un punto en el texto
        if (char == '.' and '.' in self.text):
            return
        #Si el primer caracter intruducido es un punto esto se toma como 0.
        elif(len(self.text)==0 and char == '.'):
            char = '0.'
            self.text += char
            self.display(self.text)
        elif(len(self.text) <= 12):
            self.text += char
            self.display(self.text)
        else:
            return

    def reset(self):
        self.text = ''
        self.memory = 0
        self.operation = ''
        self.display('0')
    
    def prepare(self, operation):
        #Si ya hay una operacióin guardada y hay datos para calcular
        if(self.operation and self.text and (self.operator or self.memory)):
            #print('operando en el caso con operador guardado')
            #se calculan los datos guardados y se almacena el operador para la siguiente operacion
            self.calculate()
            self.operation = operation
            self.special = True

        #Si no hay un operador previamente guardado, no hay nada en memoria y hay un texto
        elif(self.operation == '' and self.memory == 0 and self.text):
            #print('operando en el caso de texto y sin operador')
            self.operation = operation
            self.operator = float(self.text)
            self.text = ''
            #reinicia los valores en pantalla y en text
            self.display('0')

        #Si hay algo en memoria, no hay una operacion previa
        elif (self.memory and self.operation == ''):
            #print('operando en el caso defoult (con algo en memoria)')
            self.operation = operation
            #reinicia los valores en pantalla y en text
            self.display('0')
            self.text = ''


    def calculate(self):
        #Si hay algo en memoria le da a text el valor en la misma
        if(self.memory != 0):
            self.operator = self.memory
        #print(f'los valores a calcular son:\noperador: {self.operator}\ntexto: {self.text}\nmemoria: {self.memory}\noperacion: {self.operation}\n')
            
        #Compurueba el tipo de operacion
        if(self.operation == '+'):
            self.text = self.operator + float(self.text)

        elif(self.operation == '*'):
            self.text = self.operator * float(self.text)

        elif(self.operation == '/'):
            self.text = self.operator / float(self.text)

        elif(self.operation == '-'):
            self.text = self.operator - float(self.text)
                
        self.memory = float(self.text)
        self.display(str(self.memory))
        self.operation = ''
        self.text = ''
        #print(f'los valores resultantes son:\noperador: {self.operator}\ntexto: {self.text}\nmemoria: {self.memory}\noperacion: {self.operation}\n________________________________________')


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(480)
        self.setFixedHeight(360)
        self.setWindowTitle("Calculadora")
        
        #Se cargan los estilos desde el fichero qss
        with open(absPath("Scalcula.qss")) as styles:
            self.setStyleSheet(styles.read())

        self.setLayout(QGridLayout())
        self.calculadora = Calculator()
        self.layout().addWidget(self.calculadora, 0, 0, 1, 0)
        #Matriz de simbolos
        simbolos = [
            ['7','8','9','/'],
            ['4','5','6', '*'],
            ['1','2','3', '-'],
            ['.','0','=', '+'],
            ['RESET']
        ]
        #Se recorre la matriz y se le da el texto correspondiente
        for i, fila in enumerate(simbolos):
            for j, simbol in enumerate(fila):
                if(i == 4):
                    boton = QPushButton(simbol)
                    boton.setStyleSheet("height: 40px; font-size:25px;")
                    boton.clicked.connect( partial(self.buttonClick,simbol) )
                    self.layout().addWidget(boton, i+1,j, 1, 0)
                else:
                    boton = QPushButton(simbol)
                    boton.setStyleSheet("height: 40px; font-size:25px;")
                    boton.clicked.connect( partial(self.buttonClick,simbol) )
                    #Se añaden los elementos al Grid Layout en la posición correspondiente, saltando la fila del resultado
                    self.layout().addWidget(boton, i+1,j)

    #Render de numeros en pantalla
    def buttonClick(self, char):
        if(char.isdigit() or char == '.'):
            self.calculadora.write(char)
        elif(char == '='):
            self.calculadora.calculate()
        elif(char == 'RESET'):
            self.calculadora.reset()
        else:
            self.calculadora.prepare(char)

if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.show()
    app.exec()
