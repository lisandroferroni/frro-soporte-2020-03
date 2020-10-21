# Implementar la función numeros_al_final(), que mueve todos los elementos numéricos
# de lista al final de esta. Devuelve la lista.


# Resolver sin utilizar lista auxiliar
def numeros_al_final(lista):
    return sorted(lista, reverse=True)


lista = ['a', '9', 'b', '4']
print(numeros_al_final(lista))
