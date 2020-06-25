from sqlalchemy.orm import sessionmaker
from practico_08.tpi.database import engine
from practico_08.tpi.models import LineaModel, ParadaModel, Base
import json

Base.metadata.create_all(engine)
Base.metadata.bind = engine
db_session = sessionmaker()
db_session.bind = engine
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

def altas():
    # alta
    datosL = DatosLinea()
    datosP = DatosParada()

    datosL.borrar_todos()
    datosP.borrar_todos()

    linea = datosL.alta(LineaModel(id=1,name="115"))
    parada = datosP.alta(ParadaModel(id=1,id_calle_ppal=2, id_calle_cruce=3))
    datosL.append_parada(linea, parada)

    with open('../1lineas.json') as json_file:
        jsonObj = json.load(json_file)
        for l in jsonObj['0']:
            print('Name: ' + l['txt']+" "+l['attrs']['idlinea'])
            linea = datosL.alta( LineaModel( id=int(l['attrs']['idlinea']), name=l['txt']) )
            print(linea)


if __name__ == '__main__':
    altas()
