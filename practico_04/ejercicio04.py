## 4. Ejercicio al Formulario del Ejercicio 3 ,  agrege  los siguientes botones 1- un  botón  Alta 
## que inicia otra venta donde puedo ingresar una ciudad y su código postal .
## 2 – un botón Baja que borra del listad de ciudades la ciudad que esta selecionada en Treeview .
## 3 – un botón Modificar . Todos los cambios se deben ver reflejados en la lista que se muestra . 

"""
import tkinter as tk
from tkinter import ttk
from tkinter import *

class Application(tk.Frame):

    def __init__(self, window):
        super().__init__(window)
        window.title("Vista de árbol en Tkinter")

        self.treeview = ttk.Treeview(self, columns=("codigo"))
        self.treeview.heading("#0", text="Ciudad")
        self.treeview.heading("codigo", text="Codigo Postal")
        self.treeview.pack()

        self.treeview.insert("", tk.END, text="Rosario", values=("1"))
        self.treeview.insert("", tk.END, text="Buenos Aires", values=("2"))
        self.treeview.insert("", tk.END, text="Mendoza", values=("3"))
        self.treeview.insert("", tk.END, text="La Plata", values=("4"))
        self.treeview.insert("", tk.END, text="Cordoba", values=("5"))

        self.btnDivision = Button(window, text="/", command=btnDivision_click)
        self.btnDivision.pack(side="bottom")

        self.pack()


def btnDivision_click():
    secondarywindow = tk.Tk()
    secondarywindow.title("Calculadora")
    secondarywindow.geometry('400x400')

window = tk.Tk()
window.title("Calculadora")



app = Application(window)

window.mainloop()
"""
