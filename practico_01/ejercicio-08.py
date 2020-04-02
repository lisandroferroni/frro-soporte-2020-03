# Implementar la función mitad(), que devuelve la mitad de palabra.
# Si la longitud es impar, redondear hacia arriba.
import math

# hola -> ho
# verde -> ver
def mitad(palabra):
    mitad_palabra = ""
    for x in range(math.ceil(len(palabra)/2)):
        mitad_palabra += palabra[x]
    return mitad_palabra


assert mitad("hola") == "ho"
assert mitad("verde") == "ver"
