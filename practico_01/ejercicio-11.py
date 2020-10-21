# Implementar la función es_primo(), que devuelva un booleano en base a
# si numero es primo o no.


def es_primo(numero):
    if(numero < 3):
        return True
    for x in range(2, numero):
        if numero % x == 0:
            return False
    return True


assert es_primo(1)
assert es_primo(2)
assert not es_primo(10)
assert es_primo(17)
assert es_primo(113)
