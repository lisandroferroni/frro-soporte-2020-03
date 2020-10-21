## 1 Ejercicio Hacer un formulario tkinter que es una calculadora, tiene 2 entry para ingresar los valores V1 y V2.
## Y 4 botones de operaciones para las operaciones respectivas + , - , * , / ,
## al cliquearlos muestre el resultado de aplicar el operador respectivo en los V1 y V2 . 
 

from tkinter import *


def btnSuma_click():
    try:
        resultado = int(txt1.get()) + int(txt2.get())
        labelResultado.configure(text=str(resultado))
    except:
        labelResultado.configure(text="Error")



def btnResta_click():
    try:
        resultado = int(txt1.get()) - int(txt2.get())
        labelResultado.configure(text=str(resultado))
    except:
        labelResultado.configure(text="Error")


def btnMultiplicacion_click():
    try:
        resultado = int(txt1.get()) * int(txt2.get())
        labelResultado.configure(text=str(resultado))
    except:
        labelResultado.configure(text="Error")


def btnDivision_click():
    try:
        resultado = int(txt1.get()) / int(txt2.get())
        labelResultado.configure(text=str(resultado))
    except:
        labelResultado.configure(text="Error")



window = Tk()
window.title("Calculadora")
window.geometry('400x400')

labelResultado = Label (window, text="0")
labelResultado.grid(column=3, row=5)

btnSuma = Button(window, text="+", command=btnSuma_click)
btnResta = Button(window, text="-", command=btnResta_click)
btnMultiplicacion = Button(window, text="*", command=btnMultiplicacion_click)
btnDivision = Button(window, text="/", command=btnDivision_click)

btnSuma.grid(column=3, row=1)
btnResta.grid(column=4, row=1)
btnMultiplicacion.grid(column=3, row=2)
btnDivision.grid(column=4, row=2)

txt1 = Entry(window,width=10)
txt1.grid(column=1, row=0)

txt2 = Entry(window,width=10)
txt2.grid(column=10, row=0)
window.mainloop()
