# Implementar la función organizar_estudiantes() que tome como parámetro una lista de Estudiantes
# y devuelva un diccionario con las carreras como keys, y la cantidad de estudiantes en cada una de ellas como values.

from practico_02.ejercicio_04 import Estudiante


def organizar_estudiantes(estudiantes):
    diccionario = {}
    for e in estudiantes:
        if e.carrera in diccionario:
            diccionario[e.carrera] = diccionario[e.carrera] + 1
        else:
            diccionario[e.carrera] = 1
    return diccionario

estudiante1 = Estudiante("ISI", 2015,100,2,"Juan Diaz", 23, "H", 72, 1.73)
estudiante2 = Estudiante("Q", 2015,100,2,"Juan Diaz", 23, "H", 72, 1.73)
estudiante3 = Estudiante("Q", 2015,100,2,"Juan Diaz", 23, "H", 72, 1.73)
estudiante4 = Estudiante("IM", 2015,100,2,"Juan Diaz", 23, "H", 72, 1.73)


"""
carreras = organizar_estudiantes([estudiante1,estudiante2,estudiante3,estudiante4])
print(carreras)
"""
