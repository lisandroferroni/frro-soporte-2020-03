## 4. Ejercicio al Formulario del Ejercicio 3 ,  agrege  los siguientes botones 1- un  botón  Alta 
## que inicia otra venta donde puedo ingresar una ciudad y su código postal .
## 2 – un botón Baja que borra del listad de ciudades la ciudad que esta selecionada en Treeview .
## 3 – un botón Modificar . Todos los cambios se deben ver reflejados en la lista que se muestra . 


import tkinter as tk
from tkinter import ttk
from tkinter import *

class Application(tk.Frame):

    def __init__(self, window):
        self.root=window
        super().__init__(window)
        window.title("Ciudades")

        self.treeview = ttk.Treeview(self, columns=("codigo"))
        self.treeview.heading("#0", text="Ciudad")
        self.treeview.heading("codigo", text="Codigo Postal")
        self.treeview.pack()

        self.treeview.insert("", tk.END, text="Rosario", values="1")
        self.treeview.insert("", tk.END, text="Buenos Aires", values="2")
        self.treeview.insert("", tk.END, text="Mendoza", values="3")
        self.treeview.insert("", tk.END, text="La Plata", values="4")
        self.treeview.insert("", tk.END, text="Cordoba", values="5")

        self.btnAlta = Button(window, text="Alta", command= lambda: self.new_window(Win2)).pack(side="bottom")
        self.btnBaja = Button(window, text="Borrar", command=self.remove_item).pack(side="bottom")
        self.btnEdicion = Button(window, text="Editar", command=lambda: self.new_window(Win2, self.treeview.selection())).pack(side="bottom")

        self.pack()

    def remove_item(self):
       selected_items = self.treeview.selection()
       for selected_item in selected_items:
          self.treeview.delete(selected_item)


    def new_window(self, _class, item = False):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.root)
            if (not item):
                _class(self.new)
            else:
                _class(self.new, "Editar", self.treeview.item(item)["text"], self.treeview.item(item)["values"], item)

    def alta(self, nombreCiudad, codigo):
        self.treeview.insert("", tk.END, text=nombreCiudad, values=(str(codigo)))


class Win2:
    def __init__(self, root, txtBtnAgregar = "Agregar Ciudad", textoNombreCiudad = "", textoCodigo = "", item = False):

        self.root = root
        self.root.geometry("300x200+200+200")

        labelNombre = Label(self.root, text="Nombre Ciudad:")
        labelNombre.pack(side="top")

        entryTextCiudad = tk.StringVar()
        txtCiudad = Entry(self.root, width=10, textvariable=entryTextCiudad)
        entryTextCiudad.set(textoNombreCiudad)
        txtCiudad.pack(side="top")

        labelCodigo = Label(self.root, text="Codigo:")
        labelCodigo.pack(side="top")

        entryTextCodigo = tk.StringVar()
        txtCodigo = Entry(self.root, width=10, textvariable=entryTextCodigo)
        entryTextCodigo.set(textoCodigo)
        txtCodigo.pack(side="top")

        btnAgregar = Button(self.root, text=txtBtnAgregar, command=lambda: btnAgregar_click(root, txtCiudad.get(), txtCodigo.get(), item))
        btnAgregar.pack(side="bottom")


def btnAgregar_click(window, nombre, codigo, item = False):
    if (item):
        app.treeview.delete(item)
    app.alta(nombre, codigo)

    window.destroy()


window = tk.Tk()
window.title("Formulario")
app = Application(window)
window.mainloop()
secondarywindow = tk.Tk()

