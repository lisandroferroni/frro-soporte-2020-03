from sqlalchemy.orm import sessionmaker, scoped_session
from practico_08.tpi.database import engine
from practico_08.tpi.models import LineaModel, ParadaModel, Base
import json
import requests

Base.metadata.create_all(engine)
Base.metadata.bind = engine
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
session = db_session()

class DatosLinea(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, linea):
        """
        Devuelve la Linea luego de darlo de alta.
        :type linea: Linea
        :rtype: Linea
        """
        self.session.add(linea)
        self.session.commit()
        return linea

    def append_parada(self, linea, parada):
        linea.paradas.append(parada)
        self.session.commit()
        return

    def borrar_todos(self):
        """
        Borra todos las lineas de la base de datos.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        try:
            self.session.query(LineaModel).delete()
            self.session.commit()
        except:
            return False
        else:
            return True

    def buscar(self, id_linea):
        """
        Devuelve la instancia de una linea, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.session.query(LineaModel).get(id_linea)

    def getParadas(self, id_linea):
        linea = self.session.query(LineaModel).get(id_linea)
        return linea.paradas

class DatosParada(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, parada):
        """
        Devuelve la Linea luego de darlo de alta.
        :type linea: Linea
        :rtype: Linea
        """
        self.session.add(parada)
        self.session.commit()
        return parada

    def borrar_todos(self):
        """
        Borra todos las paradas de la base de datos.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        try:
            self.session.query(ParadaModel).delete()
            self.session.commit()
        except:
            return False
        else:
            return True

    def buscar(self, id_parada):
        """
        Devuelve la instancia de una parada, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Socio
        """
        return self.session.query(ParadaModel).get(id_parada)

    def getLineas(self, id_parada):
        parada = self.session.query(ParadaModel).get(id_parada)
        return parada.lineas

def altas():
    # alta
    datosL = DatosLinea()
    datosP = DatosParada()

    datosL.borrar_todos()
    datosP.borrar_todos()

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
                linea = datosL.alta( LineaModel( id=int(json["id"]), name=json['nombre']) )
                print(linea)
                for p in json["paradas"]:
                    parada = datosP.alta(ParadaModel(id=p["id"], id_calle_ppal=0, id_calle_cruce=0))
                    datosL.append_parada(linea, parada)
            except Exception as e:
                print(e)
                print(i+1, " NOT AVAILABLE")

if __name__ == '__main__':
    altas()
