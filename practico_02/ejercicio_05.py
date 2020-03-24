# Implementar la función organizar_estudiantes() que tome como parámetro una lista de Estudiantes
# y devuelva un diccionario con las carreras como keys, y la cantidad de estudiantes en cada una de ellas como values.

from practico_02.ejercicio_04 import Estudiante


def organizar_estudiantes(estudiantes):
    diccionario = {}

    #Distinct carreras
    carreras = []
    for estudiante in estudiantes:
        existe_carrera = False
        for carrera in carreras:
            if estudiante.carrera == carrera:
                existe_carrera = True
        if not existe_carrera:
            carreras.append(estudiante.carrera)

    #Count carreras
    for carrera in carreras:
        count = 0
        for estudiante in estudiantes:
            if carrera == estudiante.carrera:
                count += 1
        diccionario[carrera] = count
    return diccionario


estudiantes = [Estudiante("ISI", 2, 50, 15, "Juan Diaz", 21, "H", 72, 1.73),
               Estudiante("ISI", 1, 50, 1, "Carlos", 20, "H", 72, 1.73),
               Estudiante("Quimica", 4, 60, 15, "Maria", 25, "M", 72, 1.73),
               Estudiante("Quimica", 4, 60, 20, "Sol", 26, "M", 72, 1.73),
               Estudiante("ISI", 4, 50, 5, "Pedro", 22, "H", 72, 1.73)]
"""
diccionario = organizar_estudiantes(estudiantes)
for key in diccionario:
  print (key, ":", diccionario[key])
"""
