# Escribir una clase Estudiante, que herede de Persona, y que agregue las siguientes condiciones:
# Atributos:
# - nombre de la carrera.
# - año de ingreso a la misma.
# - cantidad de materias de la carrera.
# - cantidad de materias aprobadas.
# Métodos:
# - avance(): indica que porcentaje de la carrera tiene aprobada.
# - edad_ingreso(): indica que edad tenia al ingresar a la carrera (basándose en el año actual).
from random import randint
from practico_02.ejercicio_03 import Persona
import datetime

class Estudiante(Persona):

    def __init__(self, carrera, anio, cantidad_materias, cantidad_aprobadas, nombre, edad, sexo, peso, altura):
        Persona.__init__(self, nombre, edad, sexo, peso, altura)
        self.carrera = carrera
        self.anio = anio
        self.cantidad_materias = cantidad_materias
        self.cantidad_aprobadas = cantidad_aprobadas

    def avance(self):
        return self.cantidad_aprobadas / self.cantidad_materias * 100

    # implementar usando modulo datetime
    def edad_ingreso(self):
        return self.edad - (datetime.datetime.now().year - self.anio)

    def print_data(self):
        super().print_data()
        print("Carrera: " + self.carrera + "\nAño: " + str(self.anio) +
            "\nCantidad de materias: " + str(self.cantidad_materias) + "\nCantidad de aprobadas: " + str(self.cantidad_aprobadas))


estudiante = Estudiante("ISI", 2015, 50, 10, "Juan Diaz", 23, "H", 72, 1.73)
assert estudiante.avance() == 20
assert estudiante.edad_ingreso() == 18

estudiante.print_data()

