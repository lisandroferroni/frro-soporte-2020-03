from practico_08.tpi.models import LineaModel, ParadaModel
from practico_08.tpi.data import DatosLinea, DatosParada
import requests

class LineaExistente(Exception):
    def __str__(self):
        return('Ya existe una linea con dicho id.')
    pass
class ParadaExistente(Exception):
    def __str__(self):
        return('Ya existe una parada con dicho id.')
    pass

class LineaNegocio(object):
    def __init__(self):
        self.lineas = DatosLinea()

    def alta(self, linea):
        """
        Da de alta una linea.
        :type socio: Linea
        :rtype: bool
        """
        if(self.regla_1(linea)):
            self.lineas.alta(linea)
            return True
        return False

    def regla_1(self, socio):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        if(self.lineas.buscar(socio.id) != None):
            raise LineaExistente
        else:
            return True
        return False

    def getParadas(self, id_linea):
        return self.lineas.getParadas(id_linea)

class ParadaNegocio(object):
    def __init__(self):
        self.paradas = DatosParada()

    def alta(self, parada):
        if(self.regla_1(parada)):
            self.paradas.alta(parada)
            return True
        return False

    def regla_1(self, parada):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: DniRepetido
        :return: bool
        """
        if(self.paradas.buscar(parada.id) != None):
            raise ParadaExistente
        else:
            return True
        return False

    def getLineas(self, id_parada):
        return self.paradas.getLineas(id_parada)


def altas():
    # alta
    negocioL = LineaNegocio()
    negocioP = ParadaNegocio()

    negocioL.lineas.borrar_todos()
    negocioP.paradas.borrar_todos()

    #GET
    for i in range(96):
        if i+1 != 39 and i+1 != 41 and i+1 != 42:
            r = requests.get('https://ws.rosario.gob.ar/ubicaciones/public/linea/1/'+str(i+1)+'?conGeometria=true&usarCoordenadasWGS84=true&conParadas=true')
            try:
                json = r.json()
                print("ID LINEA ", i+1, " | Nombre linea ", json["nombre"], " | Paradas ",len(json["paradas"]))
                lineaObj = LineaModel( id=int(json["id"]), name=json['nombre'])
                linea = negocioL.alta( lineaObj )
                for p in json["paradas"]:
                    try:
                        paradaObj = ParadaModel(id=int(p["id"]), id_calle_ppal=0, id_calle_cruce=0)
                    except Exception as e:
                        print("Creating Parada ", e)
                    finally:
                        app_linea_parada = negocioL.lineas.append_parada(lineaObj, paradaObj)
                        print( "Append parada ", int(p["id"])," to linea: ", int(json["id"]) )
            except Exception as e:
                print(e)
                print("Linea con ID ",i+1, " no existe")

def boletos():
    negocioL = LineaNegocio()
    negocioP = ParadaNegocio()
    lineas_paradas = negocioL.lineas.getParadas(1)
    for lp in lineas_paradas:
        print(lp.linea_id)

if __name__ == '__main__':
    altas()
    #boletos()
