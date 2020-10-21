## 2 Ejercicio Hacer un formulario en Tkinter una calculadora que tenga 1 entry y 12 botones para los dígitos 0 al 9
## y las operaciones + - / * = , que al apretar cada botón vaya agregando al valor que muestra en el entry el carácter 
## que le corresponde ( como se ve imagen ) y cuando se aprieta en = pone el resultado de evaluar la cadena entrada . 
from tkinter import *
import re


def btnIgual_click():
    try:
        if (labelResultado["text"] == "0"):
            pass
        valores = re.findall("([0-9]+)([\+\-*\/])?",labelResultado["text"])

        if valores:
            for i in range(0,len(valores)):
                if i==0:
                    resultado=int(valores[i][0])
                else:
                    if operacion == "+":
                        resultado = resultado+int(valores[i][0])
                    elif operacion == "-":
                        resultado = resultado-int(valores[i][0])
                    elif operacion == "*":
                        resultado = resultado*int(valores[i][0])
                    elif operacion == "/":
                        resultado = resultado/int(valores[i][0])

                operacion = valores[i][1]

            labelResultado.configure(text=str(resultado))
    except:
        labelResultado.configure(text="Error")


def btn0_click():
    labelResultado.configure(text=labelResultado["text"] + "0")


def btn1_click():
    labelResultado.configure(text=labelResultado["text"] + "1")


def btn2_click():
    labelResultado.configure(text=labelResultado["text"] + "2")


def btn3_click():
    labelResultado.configure(text=labelResultado["text"] + "3")


def btn4_click():
    labelResultado.configure(text=labelResultado["text"] + "4")


def btn5_click():
    labelResultado.configure(text=labelResultado["text"] + "5")


def btn6_click():
    labelResultado.configure(text=labelResultado["text"] + "6")


def btn7_click():
    labelResultado.configure(text=labelResultado["text"] + "7")


def btn8_click():
    labelResultado.configure(text=labelResultado["text"] + "8")


def btn9_click():
    labelResultado.configure(text=labelResultado["text"] + "9")


def btnSuma_click():
    labelResultado.configure(text=labelResultado["text"] + "+")


def btnResta_click():
    labelResultado.configure(text=labelResultado["text"] + "-")


def btnMultiplicacion_click():
    labelResultado.configure(text=labelResultado["text"] + "*")


def btnDivision_click():
    labelResultado.configure(text=labelResultado["text"] + "/")


def btnCA_click():
    labelResultado.configure(text="")


window = Tk()
window.title("Calculadora")
window.geometry('400x400')

labelResultado = Label(window, text="2*2")
labelResultado.grid(column=3, row=0)

btn0 = Button(window, text="0", command=btn0_click)
btn1 = Button(window, text="1", command=btn1_click)
btn2 = Button(window, text="2", command=btn2_click)
btn3 = Button(window, text="3", command=btn3_click)
btn4 = Button(window, text="4", command=btn4_click)
btn5 = Button(window, text="5", command=btn5_click)
btn6 = Button(window, text="6", command=btn6_click)
btn7 = Button(window, text="7", command=btn7_click)
btn8 = Button(window, text="8", command=btn8_click)
btn9 = Button(window, text="9", command=btn9_click)
btnSuma = Button(window, text="+", command=btnSuma_click)
btnResta = Button(window, text="-", command=btnResta_click)
btnMultiplicacion = Button(window, text="*", command=btnMultiplicacion_click)
btnDivision = Button(window, text="/", command=btnDivision_click)
btnIgual = Button(window, text="=", command=btnIgual_click)
btnCA = Button(window, text="CA", command=btnCA_click)

btn0.grid(column=2, row=4)
btn1.grid(column=1, row=1)
btn2.grid(column=2, row=1)
btn3.grid(column=3, row=1)
btn4.grid(column=1, row=2)
btn5.grid(column=2, row=2)
btn6.grid(column=3, row=2)
btn7.grid(column=1, row=3)
btn8.grid(column=2, row=3)
btn9.grid(column=3, row=3)
btnSuma.grid(column=4, row=1)
btnResta.grid(column=5, row=1)
btnMultiplicacion.grid(column=4, row=2)
btnDivision.grid(column=5, row=2)
btnIgual.grid(column=3, row=4)
btnCA.grid(column=3, row=5)

window.mainloop()
