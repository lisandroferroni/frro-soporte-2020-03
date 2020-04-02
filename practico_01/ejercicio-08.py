# Implementar la función mitad(), que devuelve la mitad de palabra.
# Si la longitud es impar, redondear hacia arriba.
import math

# hola -> ho
# verde -> ver
def mitad(palabra):
    return palabra[0:math.ceil(len(palabra)/2)]


assert mitad("hola") == "ho"
assert mitad("verde") == "ver"
