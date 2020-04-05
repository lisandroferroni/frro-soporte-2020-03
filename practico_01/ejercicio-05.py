# Implementar la función es_vocal, que reciba un carácter y
# devuelva un booleano en base a si letra es una vocal o no.


# Resolver utilizando listas y el operador in.
def es_vocal(letra):
    return letra.lower() in 'aeiou'


assert es_vocal('i')
assert not es_vocal('b')
assert es_vocal('A')
