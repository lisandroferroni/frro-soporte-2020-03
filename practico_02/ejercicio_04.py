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


class Persona:

    def __init__(self, nombre, edad, sexo, peso, altura):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.peso = peso
        self.altura = altura
        self.dni = self.generar_dni()

    def es_mayor_edad(self):
        return self.edad >= 18

    # llamarlo desde __init__
    def generar_dni(self):
        return randint(10000000, 100000000)

    def print_data(self):
        print("Nombre: " + self.nombre + "\nEdad: " + str(self.edad) +
              "\nSexo: " + str(self.sexo) + "\nPeso: " + str(self.peso) +
              "\nAltura: " + str(self.altura) +
              "\nDni: " + str(self.dni))


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
        return self.edad - self.anio

"""
estudiante = Estudiante("ISI", 4, 50, 10, "Juan Diaz", 22, "H", 72, 1.73)
estudiante.print_data()
print("Cantidad materias: " + str(estudiante.cantidad_materias) +
       "\nCantidad aprobadas: " + str(estudiante.cantidad_aprobadas) +
       "\nPorcentaje aprobadas: %" + str(estudiante.avance()) +
       "\nEdad de ingreso: " + str(estudiante.edad_ingreso()))
"""
