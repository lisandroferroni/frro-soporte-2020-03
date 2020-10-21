# Implementar los metodos de la capa de negocio de socios.

from practico_05.ejercicio_01 import Socio
from practico_05.ejercicio_02 import DatosSocio


class DniRepetido(Exception):
    def __str__(self):
        return('Ya exite un socio con dicho DNI.')
    pass


class LongitudInvalida(Exception):
    def __str__(self):
        return('El nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.')
    pass


class MaximoAlcanzado(Exception):
    def __str__(self):
        return('Se ha excedido la cantidad máxima de socios permitida.')
    pass


class NegocioSocio(object):

    MIN_CARACTERES = 3
    MAX_CARACTERES = 15
    MAX_SOCIOS = 200

    def __init__(self):
        self.datos = DatosSocio()

    def buscar(self, id_socio):
        """
        Devuelve la instancia del socio, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar(id_socio)

    def buscar_dni(self, dni_socio):
        """
        Devuelve la instancia del socio, dado su dni.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.datos.buscar_dni(dni_socio)

    def todos(self):
        """
        Devuelve listado de todos los socios.
        :rtype: list
        """
        return self.datos.todos()

    def alta(self, socio):
        """
        Da de alta un socio.
        Se deben validar las 3 reglas de negocio primero.
        Si no validan, levantar la excepcion correspondiente.
        Devuelve True si el alta fue exitoso.
        :type socio: Socio
        :rtype: bool
        """
        if(self.regla_1(socio) and self.regla_2(socio) and self.regla_3()):
            self.datos.alta(socio)
            return True
        return False

    def baja(self, id_socio):
        """
        Borra el socio especificado por el id.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        rta = self.datos.baja(id_socio)
        return rta

    def modificacion(self, socio):
        """
        Modifica un socio.
        Se debe validar la regla 2 primero.
        Si no valida, levantar la excepcion correspondiente.
        Devuelve True si la modificacion fue exitosa.
        :type socio: Socio
        :rtype: bool
        """
        if(self.regla_2(socio)):
            return self.datos.modificacion(socio) is not None
        return False

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        if(self.buscar_dni(socio.dni) != None):
            raise DniRepetido
        else:
            return True
        return False

    def regla_2(self, socio):
        """
        Validar que el nombre y el apellido del socio cuenten con mas de 3 caracteres pero menos de 15.
        :type socio: Socio
        :raise: LongitudInvalida
        :return: bool
        """
        if(len(socio.nombre) > self.MIN_CARACTERES and len(socio.nombre) < self.MAX_CARACTERES and len(socio.apellido) > self.MIN_CARACTERES and len(socio.apellido) < self.MAX_CARACTERES):
            return True
        else:
            raise LongitudInvalida


    def regla_3(self):
        """
        Validar que no se esta excediendo la cantidad maxima de socios.
        :raise: MaximoAlcanzado
        :return: bool
        """
        if( len(self.todos()) > self.MAX_SOCIOS ):
            raise MaximoAlcanzado
        return True

