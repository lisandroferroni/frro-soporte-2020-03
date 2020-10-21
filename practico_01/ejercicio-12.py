# Determinar la suma de todos los numeros de 1 a N. N es un número que se ingresa
# por consola.


def suma(N):
    return sum(list(range(1, N+1)))

print(suma(int(input())))
