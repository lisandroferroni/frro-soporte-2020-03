from practico_06.capa_negocio import *

import tkinter as tk
from tkinter import ttk
from tkinter import *

class Application(tk.Frame):

    def __init__(self, window):
        self.root=window
        super().__init__(window)
        self.negocio = NegocioSocio()
        window.title("ABM Socios")

        self.treeview = ttk.Treeview(self, columns=("nombre", "apellido", "dni"))
        self.treeview.heading("#0", text="Id")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("apellido", text="Apellido")
        self.treeview.heading("dni", text="DNI")
        self.treeview.pack()

        for s in self.negocio.todos():
            self.treeview.insert("", tk.END, text=s.id, values=(s.nombre, s.apellido, s.dni))

        self.btnAlta = Button(window, text="Alta", command= lambda: self.new_window(Win2)).pack(side="bottom")
        self.btnBaja = Button(window, text="Borrar", command=self.remove_item).pack(side="bottom")
        self.btnEdicion = Button(window, text="Editar", command=lambda: self.new_window(Win2, self.treeview.selection())).pack(side="bottom")

        self.pack()

    def remove_item(self):
       selected_items = self.treeview.selection()
       for selected_item in selected_items:
            item = self.treeview.item(selected_item)
            self.negocio.baja(item["text"])
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
                _class(self.new, "Editar",
                    self.treeview.item(item)["values"][0], self.treeview.item(item)["values"][1], self.treeview.item(item)["values"][2],
                item)

    def alta(self, idSocio, nombreSocio, apellidoSocio, dniSocio):
        self.treeview.insert("", tk.END, text=idSocio, values=(nombreSocio, apellidoSocio, dniSocio))


class Win2:
    def __init__(self, root, txtBtnAgregar = "Agregar Socio", textoNombreSocio = "", textoCodigo = "", textoDNI = "", item = False):

        self.root = root
        self.root.geometry("300x200+200+200")

        ###################################################
        labelNombre = Label(self.root, text="Nombre Socio:")
        labelNombre.pack(side="top")

        entryTextNombre = tk.StringVar()
        txtNombre = Entry(self.root, width=10, textvariable=entryTextNombre)
        entryTextNombre.set(textoNombreSocio)
        txtNombre.pack(side="top")

        ###################################################
        labelApellido = Label(self.root, text="Apellido:")
        labelApellido.pack(side="top")

        entryTextApellido = tk.StringVar()
        txtApellido = Entry(self.root, width=10, textvariable=entryTextApellido)
        entryTextApellido.set(textoCodigo)
        txtApellido.pack(side="top")

        ###################################################
        labelDNI = Label(self.root, text="DNI:")
        labelDNI.pack(side="top")

        entryTextDNI = tk.StringVar()
        txtDNI = Entry(self.root, width=10, textvariable=entryTextDNI)
        entryTextDNI.set(textoDNI)
        txtDNI.pack(side="top")

        btnAgregar = Button(self.root, text=txtBtnAgregar, command=lambda: btnAgregar_click(root, txtNombre.get(), txtApellido.get(), txtDNI.get(), item))
        btnAgregar.pack(side="bottom")
        btnCancel = Button(self.root, text="Cancelar", command=lambda: self.root.destroy())
        btnCancel.pack(side="bottom")


def btnAgregar_click(window, nombre, apellido, dni, item = False):
    if (item): #Caso edición
        item_selected = app.treeview.item(item)
        app.treeview.delete(item)
        socio_modif = Socio(id=item_selected["text"], dni=dni, nombre=nombre, apellido=apellido)
        app.negocio.modificacion(socio_modif)
        app.alta(item_selected["text"], nombre, apellido, dni)
        window.destroy()
        return
    socio = Socio(dni=dni, nombre=nombre, apellido=apellido)
    alta = app.negocio.alta(socio)
    if(alta): #Caso alta
        socio_bd = app.negocio.buscar_dni(dni)
        app.alta(socio_bd.id, nombre, apellido, dni)
    window.destroy()


window = tk.Tk()
window.title("Formulario")
app = Application(window)
window.mainloop()
secondarywindow = tk.Tk()
