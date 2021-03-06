from practico_08.tpi.models import LineaModel, ParadaModel, CalleModel, InterseccionModel, BoletoModel, CuadroModel
from practico_08.tpi.data import DatosLinea, DatosParada, DatosCalle, DatosInterseccion, DatosBoleto, DatosCuadro, DatosStoredProcedure
from practico_08.tpi.helpers import normal_dates
import requests
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, time
import random

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
        if(self.intersecciones.buscar({'id_linea': interseccion.id_linea, 'id_parada': interseccion.id_parada}) != None):
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


class BoletoNegocio(object):
    def __init__(self):
        self.boletos = DatosBoleto()

    def alta(self, boleto):
        self.boletos.alta(boleto)


class CuadroNegocio(object):
    def __init__(self):
        self.cuadros = DatosCuadro()

    def alta(self, cuadro):
        self.cuadros.alta(cuadro)

    def getCuadroByLineaParada(self, numLinea, numParada):
        return self.cuadros.getCuadroByLineaParada(numLinea, numParada)


class StoredProcedureNegocio(object):
    def __init__(self):
        self.sp = DatosStoredProcedure()

    def cuandoLlego(self, deltaDias, fecha, linea, parada):
        return self.sp.cuandoLlego(deltaDias, fecha, linea, parada)

    def createCuandoLlegoSP(self):
        self.sp.createProcedure()



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

                #Lineas
                lineaObj = LineaModel(id=int(json["id"]), name=json['nombre'])
                negocioL.alta(lineaObj)

                #Paradas
                for p in json["paradas"]:
                    try:
                        paradaObj = ParadaModel(id=int(p["id"]))
                        negocioP.alta(paradaObj)
                    except Exception as e:
                        print("Creating Parada error: ", e)

                #Calles
                c = requests.post('http://www.emr.gov.ar/ajax/cuandollega/getInfoParadas.php',
                    data = {'accion':'getCalle', 'idLinea': cllego_emr[json["codigoEMR"]]})
                json_calle = c.json()
                for calle in json_calle:
                    try:
                        calleObj = CalleModel(id=int(calle["id"]), nombre=calle["desc"])
                        print('Nueva calle 1: ', calleObj.id, ' - ',calleObj.nombre)
                        negocioC.alta(calleObj)
                    except Exception as e:
                        print("Creating Calle 2: ", e)
                    try:
                        c_i = requests.post('http://www.emr.gov.ar/ajax/cuandollega/getInfoParadas.php',
                            data = {'accion':'getInterseccion', 'idLinea': cllego_emr[json["codigoEMR"]], 'idCalle': int(calle["id"])})
                        json_interseccion = c_i.json()
                        for inter in json_interseccion:
                            try:
                                calle2Obj = CalleModel(id=int(inter["id"]), nombre=inter["desc"])
                                print('/////////////Nueva calle 2: ', calle2Obj.id, ' - ', calle2Obj.nombre)
                                negocioC.alta(calle2Obj)
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
                                paradaObj = ParadaModel(id=int(p["id"]))
                                interObj = InterseccionModel(id_linea=int(json["id"]), id_calle_1=int(calle["id"]), id_calle_2=int(inter["id"]), id_parada=int(id_a_parada))
                                negocioI.alta(interObj)
                            except Exception as e:
                                print("Creating intersección error:", e)
                    except Exception as e:
                        print("Creating Calle 2 & Intersección: ", e)

            except Exception as e:
                print(e)
                print("Linea con ID ",i+1, " no existe")

def boletos():
    negocioB = BoletoNegocio()
    negocioL = LineaNegocio()
    negocioB.boletos.borrar_todos()
    now = datetime.now()
    yest = now - timedelta(days=1)
    print('Cantidad de lineas: ', len(negocioL.lineas.all()))
    for l in negocioL.lineas.all(): #Cada línea de colectivo
        print('----------Cantidad de paradas: ', len(negocioL.lineas.getParadas(l.id)))
        for p in negocioL.lineas.getParadas(l.id): #Cada parada de cada línea de colectivo
            now = datetime.now()
            for i in range(30):  # Cada día de los últimos 30.
                print(i+1)
                yest = now - timedelta(days=1)
                print(yest.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
                qty = random.randint(1, 10)
                dates = normal_dates(yest.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"), qty)
                now = yest
                for d in dates:
                    boleto = BoletoModel(id_linea=l.id, id_parada=p.id, created_date=d)
                    negocioB.alta(boleto)

def crearBoletos():
    numLinea = 1
    numParada = 1141
    cantidadDeBoletosPorParada = 3
    cantidadDiasACargar = 125

    negocioB = BoletoNegocio()
    negocioC = CuadroNegocio()
    cuadro = negocioC.getCuadroByLineaParada(numLinea, numParada)

    for horario in cuadro:
        now = datetime.now()
        dia = datetime(now.year, now.month, now.day, horario.hora.hour, horario.hora.minute, 0)
        id_cuadro = horario.id
        print(dia)

        for i in range(cantidadDiasACargar):
            dia = dia - timedelta(days=1)
            horarioReal = datetime.strptime(normal_dates((dia - timedelta(minutes=(2))).strftime("%Y-%m-%d %H:%M:%S"), (dia + timedelta(minutes=(15))).strftime("%Y-%m-%d %H:%M:%S"), 1)[0], "%Y-%m-%d %H:%M:%S")
            dates = normal_dates((horarioReal - timedelta(minutes=(1))).strftime("%Y-%m-%d %H:%M:%S"), (horarioReal + timedelta(minutes=(1))).strftime("%Y-%m-%d %H:%M:%S"), cantidadDeBoletosPorParada)
            for d in dates:
                genero = 0
                tipo = 'Normal'

                probGenero = random.random()
                probTipo = random.random()

                if (horarioReal.hour >= 20 or horarioReal.hour < 7):
                    if (probGenero > 0.2):
                        genero = 0
                    else:
                        genero = 1
                else:
                    if (probGenero > 0.4):
                        genero = 0
                    else:
                        genero = 1

                if (0 < probTipo <= 0.1):
                    tipo = 'Medio'
                elif (0.1 < probTipo <= 0.2):
                    tipo = 'Pase'
                elif (0.2 < probTipo <= 0.28):
                    tipo = 'Jubilado'
                elif (0.28 < probTipo <= 1):
                    tipo = 'Normal'


                boleto = BoletoModel(id_linea=numLinea, id_parada=numParada, created_date=d, id_cuadro=id_cuadro, genero=genero, tipo=tipo)
                negocioB.alta(boleto)
                print(d)

def crearCuadro():
    negocioC = CuadroNegocio()

    cuadro1104 = []
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(5, 18)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(6, 35)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(7, 23)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(8, 10)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(8, 55)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(9, 40)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(10, 26)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(11, 12)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(11, 58)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(12, 44)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(13, 30)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(14, 16)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(15, 2)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(15, 47)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(16, 19)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(16, 51)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(17, 23)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(18, 3)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(18, 54)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(19, 35)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(20, 19)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(21, 5)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(21, 51)))
    cuadro1104.append(CuadroModel(id_linea=1, id_parada=1104, hora=time(23, 7)))

    #for cuadroObj in cuadro1104:
    #    negocioC.alta(cuadroObj)

    cuadro1141 = []
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(5, 22)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(6, 40)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(7, 28)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(8, 15)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(9, 00)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(9, 45)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(10, 31)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(11, 17)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(12, 3)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(12, 49)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(13, 35)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(14, 21)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(15, 7)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(15, 52)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(16, 24)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(16, 56)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(17, 28)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(18, 8)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(18, 59)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(19, 40)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(20, 24)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(21, 10)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(21, 56)))
    cuadro1141.append(CuadroModel(id_linea=1, id_parada=1141, hora=time(23, 12)))

    for cuadroObj in cuadro1141:
        negocioC.alta(cuadroObj)


def createSP():
    negocioSP = StoredProcedureNegocio()
    negocioSP.createCuandoLlegoSP()


    '''
    negocioL = LineaNegocio()
    negocioP = ParadaNegocio()
    lineas_paradas = negocioL.lineas.getParadas(1)
    for lp in lineas_paradas:
        print(lp.linea_id)
    '''
if __name__ == '__main__':
    #altas()
    #boletos()
    crearBoletos()
    #crearCuadro()
    #createSP()
    pass
