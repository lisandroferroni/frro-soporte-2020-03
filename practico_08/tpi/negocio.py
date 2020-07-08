from practico_08.tpi.models import LineaModel, ParadaModel
from practico_08.tpi.data import DatosLinea, DatosParada
import requests

class LineaExistente(Exception):
    def __str__(self):
        return('Ya exite una linea con dicho id.')
    pass
class ParadaExistente(Exception):
    def __str__(self):
        return('Ya exite una parada con dicho id.')
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

    """
    linea = datosL.alta(LineaModel(id=1,name="115"))
    parada = datosP.alta(ParadaModel(id=1,id_calle_ppal=2, id_calle_cruce=3))
    datosL.append_parada(linea, parada)
    """
    """
    with open('../1lineas.json') as json_file:
        with open('../getParadas_x_idLinea.json.json') as paradas:
            jsonObj = json.load(json_file)
            for l in jsonObj['0']:
                print('Name: ' + l['txt']+" "+l['attrs']['idlinea'])
                linea = datosL.alta( LineaModel( id=int(l['attrs']['idlinea']), name=l['txt']) )
                print(linea)
    """
    #GET
    for i in range(96):
        if i+1 != 39 and i+1 != 41 and i+1 != 42:
            r = requests.get('https://ws.rosario.gob.ar/ubicaciones/public/linea/1/'+str(i+1)+'?conGeometria=true&usarCoordenadasWGS84=true&conParadas=true')
            try:
                json = r.json()
                print(i+1, json["nombre"], json["paradas"][0])
                lineaObj = LineaModel( id=int(json["id"]), name=json['nombre'])
                linea = negocioL.alta( lineaObj )
                for p in json["paradas"]:
                    paradaObj = ParadaModel(id=int(p["id"]), id_calle_ppal=0, id_calle_cruce=0)
                    parada = negocioP.alta(paradaObj)
                    negocioL.lineas.append_parada(lineaObj, paradaObj)
            except Exception as e:
                print(e)
                print(i+1, " NOT AVAILABLE")

    for l in negocioP.getLineas(6732):
        print("Linea "+l.name+" para en parada 6732")
        for p in negocioL.getParadas(l.id):
            print("*******Parada "+str(p.id)+" para en linea "+l.name)

if __name__ == '__main__':
    altas()
