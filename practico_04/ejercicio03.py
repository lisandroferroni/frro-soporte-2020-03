## 3 Ejercicio Crear un Formulario que usando el control Treeview muestre la una lista con los nombre de
## Ciudades Argentinas y su código postal ( por lo menos 5 ciudades ) . 
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

        self.pack()




window = tk.Tk()



app = Application(window)
app.mainloop()
