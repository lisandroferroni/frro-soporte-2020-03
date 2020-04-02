# Implementar la clase Persona que cumpla las siguientes condiciones:
# Atributos:
# - nombre.
# - edad.
# - sexo (H hombre, M mujer).
# - peso.
# - altura.
# Métodos:
# - es_mayor_edad(): indica si es mayor de edad, devuelve un booleano.
# - print_data(): imprime por pantalla toda la información del objeto.
# - generar_dni(): genera un número aleatorio de 8 cifras y lo guarda dentro del atributo dni.
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
              "\nDNI: " + str(self.dni))

"""
persona = Persona("Juan Diaz", 22, "H", 72, 1.73)
persona.print_data()
"""
