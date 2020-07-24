from practico_08.tpi.models import LineaModel, ParadaModel, CalleModel, InterseccionModel
from practico_08.tpi.data import DatosLinea, DatosParada, DatosCalle, DatosInterseccion
import requests
from lxml import etree
from bs4 import BeautifulSoup

class LineaExistente(Exception):
    def __str__(self):
        return('Ya existe una linea con dicho id.')
    pass
class ParadaExistente(Exception):
    def __str__(self):
        return('Ya existe una parada con dicho id.')
    pass
class CalleExistente(Exception):
    def __str__(self):
        return('Ya existe una calle con dicho id.')
    pass
class InterseccionExistente(Exception):
    def __str__(self):
        return('Ya existe una intersección con dicho id.')
    pass

class CalleNegocio(object):
    def __init__(self):
        self.calles = DatosCalle()

    def alta(self, calle):
        """
        Da de alta una linea.
        :type socio: Linea
        :rtype: bool
        """
        if(self.regla_1(calle)):
            self.calles.alta(calle)
            return True
        return False

    def regla_1(self, calle):
        """
        Validar que el id de la calle es unico (que ya no este usado).
        :type socio: Calle
        :raise: CalleExistente
        :return: bool
        """
        if(self.calles.buscar(calle.id) != None):
            raise CalleExistente
        else:
            return True
        return False

class InterseccionNegocio(object):
    def __init__(self):
        self.intersecciones = DatosInterseccion()

    def alta(self, interseccion):
        """
        Da de alta una interseccion.
        :type socio: Interseccion
        :rtype: bool
        """
        if(self.regla_1(interseccion)):
            self.intersecciones.alta(interseccion)
            return True
        return False

    def regla_1(self, interseccion):
        """
        Validar que el id de la interseccion es unico (que ya no este usado).
        :type socio: Interseccion
        :raise: InterseccionExistente
        :return: bool
        """
        if(self.intersecciones.buscar({'id_linea': interseccion.id_linea, 'id_calle_1': interseccion.id_calle_1, 'id_calle_2': interseccion.id_calle_2}) != None):
            raise InterseccionExistente
        else:
            return True
        return False

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

    def regla_1(self, linea):
        """
        Validar que el DNI del socio es unico (que ya no este usado).
        :type socio: Socio
        :raise: LineaExistente
        :return: bool
        """
        if(self.lineas.buscar(linea.id) != None):
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
    negocioC = CalleNegocio()
    negocioI = InterseccionNegocio()

    negocioL.lineas.borrar_todos()
    negocioP.paradas.borrar_todos()

    cllego_emr = {
        "101": 37,
        "102": 38, #102R es 2
        "103": 39,
        "106": 4,
        "107": 41,
        "110": 42,
        "112": 27,
        "113": 11,
        "115": 28,
        "116": 12,
        "120": 13,
        "121": 14,
        "122": 29,
        "123": 15,
        "125": 43,
        "126": 30,
        "127": 31,
        "128": 44,
        "129": 45,
        "130": 46,
        "131": 32,
        "132": 33,
        "133": 47,
        "134": 16,
        "135": 17,
        "136": 18,
        "137": 19,
        "138": 34,
        "139": 35,
        "140": 36,
        "141": 20,
        "142": 48,
        "143": 49,
        "144": 50,
        "145": 51,
        "146": 52,
        "153": 21,
        "ENO": 8,
        "K": 23,
        "RC": 26,
        "K": 23,
        "Ronda": 25,
        "EBI": 7,
        "EAO": 6,
        "ENS": 10,
        "ESL": 9,
        "Q": 24
    }

    #GET
    for i in range(96):
        if i+1 != 39 and i+1 != 41 and i+1 != 42:
            r = requests.get('https://ws.rosario.gob.ar/ubicaciones/public/linea/1/'+str(i+1)+'?conGeometria=true&usarCoordenadasWGS84=true&conParadas=true')
            try:
                json = r.json()
                print("ID LINEA ", i+1, " | Nombre linea ", json["nombre"], " | Paradas ",len(json["paradas"]), " | EMR", json["codigoEMR"])
                #Calles
                c = requests.post('http://www.emr.gov.ar/ajax/cuandollega/getInfoParadas.php',
                    data = {'accion':'getCalle', 'idLinea': cllego_emr[json["codigoEMR"]]})
                json_calle = c.json()
                for calle in json_calle:
                    try:
                        calleObj = CalleModel(id=int(calle["id"]), nombre=calle["desc"])
                        negocioC.alta(calleObj)
                        c_i = requests.post('http://www.emr.gov.ar/ajax/cuandollega/getInfoParadas.php',
                            data = {'accion':'getInterseccion', 'idLinea': cllego_emr[json["codigoEMR"]], 'idCalle': int(calle["id"])})
                        json_interseccion = c_i.json()
                        for inter in json_interseccion:
                            try:
                                calleObj = CalleModel(id=int(inter["id"]), nombre=inter["desc"])
                                negocioC.alta(calleObj)
                            except Exception as e:
                                print("Creating calle error:", e)
                            try:
                                #Vínculo intersección - parada
                                i_p = requests.post('http://www.emr.gov.ar/ajax/cuandollega/getInfoParadas.php',
                                    data = {'accion':'getParadasXCalles', 'idLinea': cllego_emr[json["codigoEMR"]], 'idCalle': int(calle["id"]),'txtLinea': json["codigoEMR"], 'idInt': int(inter["id"])})
                                soup = BeautifulSoup(i_p.text,'lxml')
                                anchors = soup.find_all('a')
                                if(len(anchors) > 0):
                                    id_a_parada = anchors[0].text
                                else:
                                    id_a_parada = 0
                                #Intersección
                                print("Agregando intersección.")
                                interObj = InterseccionModel(id_linea=int(json["id"]), id_calle_1=int(calle["id"]), id_calle_2=int(inter["id"]), id_parada=int(id_a_parada))
                                negocioI.alta(interObj)
                            except Exception as e:
                                print("Creating intersección error:", e)
                    except Exception as e:
                        print("Creating Parada ", e)
                #Lineas
                lineaObj = LineaModel( id=int(json["id"]), name=json['nombre'])
                linea = negocioL.alta( lineaObj )
                for p in json["paradas"]:
                    try:
                        paradaObj = ParadaModel(id=int(p["id"]))
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
