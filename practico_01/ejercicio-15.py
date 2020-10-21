# Reescribe el programa que pide al usuario una lista de números e imprime en
# pantalla el máximo y mínimo de los números introducidos al final,cuando el usuario
# introduce “fin”. Escribe ahora el programa de modo que almacene los números que
# el usuario introduzca en una lista y usa las funciones Max () y min () para calcular los
# números máximo y mínimo después de que el bucle termine.

array = []
var = input()
while var != "fin":
    array.append(var)
    var = input()
print(f"Maximo: {max(array)}\nMinimo: {min(array)}")
