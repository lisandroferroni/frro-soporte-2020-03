import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from practico_08.tpi.database import engine
from practico_08.tpi.models import BoletoModel, LineaModel, ParadaModel, CalleModel, InterseccionModel, CuadroModel, Base
import json
import requests
import datetime

Base.metadata.create_all(engine)
Base.metadata.bind = engine
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
session = db_session()

class DatosCalle(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, calle):
        """
        Devuelve la Calle luego de darla de alta.
        :type linea: Calle
        :rtype: Calle
        """
        self.session.add(calle)
        self.session.commit()
        return calle

    def buscar(self, calle_id):
        """
        Devuelve la calle de una intersección, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Calle
        """
        return self.session.query(CalleModel).get(calle_id)

class DatosInterseccion(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, interseccion):
        """
        Devuelve la Intersección luego de darla de alta.
        :type linea: Intersección
        :rtype: Intersección
        """
        try:
            self.session.add(interseccion)
            self.session.commit()
            return interseccion
        except Exception as e:
            print("Error appending interseccion", e)
            print("Rolling back append")
            self.session.rollback()
        finally:
            return

    def buscar(self, interseccionDict):
        """
        Devuelve la instancia de una intersección, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Intersección
        """
        return self.session.query(InterseccionModel).get(interseccionDict)

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
        try:
            print("Appending ", parada.id, " to ", linea.id)
            #Search for existing parada. Add new instance gave ReferenceError
            pM = DatosParada()
            p = pM.buscar(parada.id)
            if p is None:
                p = parada
            linea.paradas.append(p)
            self.session.commit()
        except Exception as e:
            print("Error appending ", e)
            print("Rolling back append")
            self.session.rollback()
        finally:
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

    def all(self):
        """
        Devuelve las instancias de lineas.
        Devuelve None si no encuentra nada.
        :rtype: [Linea]
        """
        return self.session.query(LineaModel).all()

    def buscar(self, id_linea):
        """
        Devuelve la instancia de una linea, dado su id.
        Devuelve None si no encuentra nada.
        :rtype: Linea
        """
        return self.session.query(LineaModel).get(id_linea)

    def getParadas(self, id_linea):
        intersecciones = self.session.query(InterseccionModel).filter(InterseccionModel.id_linea == id_linea)
        paradas = []
        for i in intersecciones:
            p = DatosParada.buscar(self, i.id_parada)
            if p is not None:
                paradas.append(p)
        return paradas

class DatosBoleto(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, boleto):
        """
        Devuelve la Linea luego de darlo de alta.
        :type linea: Linea
        :rtype: Linea
        """
        try:
            self.session.add(boleto)
            self.session.commit()
            return boleto
        except Exception as e:
            print("Error appending ", e)
            print("Rolling back")
            self.session.rollback()
            return e

    def borrar_todos(self):
        """
        Borra todos los boletos de la base de datos.
        Devuelve True si el borrado fue exitoso.
        :rtype: bool
        """
        try:
            self.session.query(BoletoModel).delete()
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
        try:
            self.session.add(parada)
            self.session.commit()
        except:
            print("Rolling back")
            self.session.rollback()
        finally:
            return parada

    def append_lineas(self, parada, linea):
        try:
            print("Appending ", linea.id, " to ", parada.id)
            parada.lineas.append(linea)
            self.session.commit()
        except Exception as e:
            print("Error appending ", e)
            print("Rolling back append")
            self.session.rollback()
        finally:
            return

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


class DatosCuadro(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def alta(self, cuadro):
        """
        Devuelve la Linea luego de darlo de alta.
        :type cuadro: Cuadro
        :rtype: Cuadro
        """
        try:
            self.session.add(cuadro)
            self.session.commit()
            return cuadro
        except Exception as e:
            print("Error appending ", e)
            print("Rolling back")
            self.session.rollback()
            return e

    def getCuadro(self, id_cuadro):
        return self.session.query(CuadroModel).get(id_cuadro)


class DatosStoredProcedure(object):
    def __init__(self):
        self.session = session
        self.base = Base.metadata
        self.engine = engine

    def cuandoLlego(self, deltaDias, fecha, linea, parada):
        try:
            connection = engine.raw_connection()
            cursor = connection.cursor()
            cursor.callproc("CuandoLlego", [deltaDias, fecha, linea, parada])
            results = list(cursor.fetchall())
            cursor.close()
            connection.commit()
            return results[0][0]

        except Exception as e:
            print("Error calling 'CuandoLlego :", e)

    def createProcedure(self):
        try:
            query = "USE cuandollego;"
            query1 = "DROP PROCEDURE IF EXISTS CuandoLlego;"
            query2 = """CREATE PROCEDURE CuandoLlego(deltaDias INT , fecha DATETIME, linea INT, parada INT)\n\
            BEGIN\n\
                DROP TEMPORARY TABLE IF EXISTS Segundos;\n\
                CREATE TEMPORARY TABLE Segundos(Segundo INT);\n\
                SET @contador = 0;\n\
                SET @fecha = fecha;\n\
                SET @idCuadroProxHorario = 0;\n\
                SET @tipoDia = CASE WHEN WEEKDAY(fecha) < 5 THEN 0\n\
                                    WHEN WEEKDAY(fecha) = 5 THEN 1\n\
                                    ELSE 2\n\
                                    END;\n\
            \n\
                SELECT id \n\
                FROM cuadro\n\
                WHERE id_linea = linea \n\
                AND id_parada = parada\n\
                AND Hora >= TIME(DATE_ADD(fecha, INTERVAL -10 minute)) \n\
                -- AND tipo_dia = @tipoDia \n\
                ORDER BY Hora\n\
                LIMIT 1    \n\
                INTO @idCuadroProxHorario;   \n\
                \n\
                IF @idCuadroProxHorario = 0 THEN\n\
                    SELECT id \n\
                    FROM cuadro\n\
                    WHERE id_linea = linea \n\
                    AND id_parada = parada\n\
                    -- AND tipo_dia = @tipoDia\n\
                    ORDER BY Hora\n\
                    LIMIT 1\n\
                    INTO @idCuadroProxHorario;\n\
                    \n\
                END IF;\n\
            \n\
                WHILE @contador <= deltaDias DO\n\
                    SET @contador = @contador + 1;\n\
                    SET @fecha = CASE\n\
                            WHEN WEEKDAY(fecha) < 5 AND WEEKDAY(@fecha)<>0 THEN DATE_ADD(@fecha, INTERVAL -1 DAY)\n\
                            WHEN WEEKDAY(fecha) < 5 AND WEEKDAY(@fecha)=0 THEN DATE_ADD(@fecha, INTERVAL -3 DAY)\n\
                            ELSE DATE_ADD(@fecha, INTERVAL -7 DAY)\n\
                            END;\n\
            \n\
                    INSERT INTO Segundos\n\
                        SELECT TIMESTAMPDIFF(SECOND, @fecha , created_date)  \n\
                        FROM boleto\n\
                        WHERE (DATE(created_date) = DATE(@fecha)\n\
                        OR DATE(created_date) = DATE(DATE_ADD(@fecha, INTERVAL 1 DAY)))\n\
                        AND created_date > DATE_ADD(@fecha, INTERVAL -1 HOUR)\n\
                        AND id_linea = linea\n\
                        AND id_parada = parada\n\
                        AND id_cuadro =  @idCuadroProxHorario\n\
                        ORDER BY created_date\n\
                        LIMIT 1;\n\
                END WHILE;\n\
                SELECT SEC_TO_TIME(AVG(Segundo)) TiempoParaArribo from Segundos;    \n\
            END"""
            connection = engine.raw_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.execute(query1)
            cursor.execute(query2)
        except Exception as e:
            print("Error creating store procedure: ", e)


def altas():
    # alta
    datosL = DatosLinea()
    datosP = DatosParada()

    datosL.borrar_todos()
    datosP.borrar_todos()

    """
    linea = datosL.alta(LineaModel(id=1,name="115"))
    parada = datosP.alta(ParadaModel(id=1))
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





if __name__ == '__main__':
    altas()

    #sp = DatosStoredProcedure()
    #print(sp.cuandoLlego(300, datetime.datetime.utcnow(), 1, 1141))
