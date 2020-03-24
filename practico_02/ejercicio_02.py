# Implementar la clase Circulo que contiene un radio, y sus métodos area y perimetro.
import math


class Circulo:

    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return 3.14 * pow(self.radio, 2)

    def perimetro(self):
        return int(math.pi * self.radio * 2)


circulo = Circulo(10)
assert circulo.area() == 314
assert circulo.perimetro() == int(62.8)
