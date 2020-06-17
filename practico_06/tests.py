# Implementar los casos de prueba descriptos.

import unittest

from practico_05.ejercicio_01 import Socio
from practico_06.capa_negocio import NegocioSocio, LongitudInvalida, DniRepetido, MaximoAlcanzado


class TestsNegocio(unittest.TestCase):

    def setUp(self):
        super(TestsNegocio, self).setUp()
        self.ns = NegocioSocio()

    def tearDown(self):
        super(TestsNegocio, self).tearDown()
        self.ns.datos.borrar_todos()

    def test_alta(self):
        # pre-condiciones: no hay socios registrados
        self.assertEqual(len(self.ns.todos()), 0)

        # ejecuto la logica
        socio = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        exito = self.ns.alta(socio)

        # post-condiciones: 1 socio registrado
        self.assertTrue(exito)
        self.assertEqual(len(self.ns.todos()), 1)

    def test_regla_1(self):
        #ejecuto la lógica
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_1(valido))
        exito = self.ns.alta(valido)

        invalido = Socio(dni=12345678, nombre='Pedro', apellido='Lopez')
        self.assertRaises(DniRepetido, self.ns.regla_1, invalido)

    def test_regla_2_nombre_menor_3(self):
        # valida regla
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_2(valido))

        # nombre menor a 3 caracteres
        invalido = Socio(dni=12345678, nombre='J', apellido='Perez')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)

    def test_regla_2_nombre_mayor_15(self):
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_2(valido))

        # nombre mayor a 15 caracteres
        invalido = Socio(dni=12345678, nombre='JuanPacooooooooooooooooo', apellido='Perez')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)

    def test_regla_2_apellido_menor_3(self):
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_2(valido))

        # apellido menor a 3 caracteres
        invalido = Socio(dni=12345678, nombre='Juan', apellido='P')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)

    def test_regla_2_apellido_mayor_15(self):
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.assertTrue(self.ns.regla_2(valido))

        # apellido mayor a 15 caracteres
        invalido = Socio(dni=12345678, nombre='Juan', apellido='Perezzzzzzzzzzzzzzzzzzzzzzz')
        self.assertRaises(LongitudInvalida, self.ns.regla_2, invalido)

    def test_regla_3(self):
        #valido primer ingreso
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        self.assertTrue(self.ns.regla_3())

        #Inscripción de 200 socios
        dni = 3912060
        for i in range(200):
            dni = dni + 1
            socio = Socio(dni=dni, nombre='Juan El '+str(i), apellido='Perez')
            self.ns.alta(socio)
        #Inscripción de socio 201
        self.assertRaises(MaximoAlcanzado, self.ns.regla_3)

    def test_baja(self):
        #baja valida socio existente
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        self.assertTrue(self.ns.baja(valido.id))

        # baja invalida socio no inscripto
        invalido = Socio(dni=87654321, nombre='Juan', apellido='Perez')
        self.assertFalse(self.ns.baja(invalido.id))

    def test_buscar(self):
        #alta valida y búsqueda válida
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        self.assertIsNotNone(self.ns.buscar(valido.id))

        #creación y búsqueda sin alta
        invalido = Socio(dni=87654321, nombre='Pedro', apellido='Lopez')
        self.assertIsNone(self.ns.buscar(invalido.id))

    def test_buscar_dni(self):
        # busqueda valida por dni
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        self.assertIsNotNone(self.ns.buscar_dni(valido.dni))

        # creación y búsqueda por DNI sin alta
        invalido = Socio(dni=87654321, nombre='Pedro', apellido='lopez')
        self.assertIsNone(self.ns.buscar_dni(invalido.dni))

    def test_todos(self):
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        self.assertIsNotNone( self.ns.todos() )

    def test_modificacion(self):
        # modificacion valida de socio existente
        valido = Socio(dni=12345678, nombre='Juan', apellido='Perez')
        self.ns.alta(valido)
        valido_modif = Socio(id=valido.id, dni=87654321, nombre='Pedro', apellido='Lopez')
        self.assertTrue(self.ns.modificacion(valido_modif))

        # modificacion socio inexistente
        invalido = Socio(id=12312312, dni=87654321, nombre='Pedro', apellido='Lopez')
        self.assertFalse(self.ns.modificacion(invalido))
