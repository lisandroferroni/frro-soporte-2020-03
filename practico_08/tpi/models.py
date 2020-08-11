import datetime
import time
import numpy as np
from matplotlib import pyplot
from matplotlib.dates import date2num
from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()


class LineaModel(Base):
    __tablename__ = 'linea'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    #lineaParadas = relationship("LineaParadaModel", back_populates="linea")
    intersecciones = relationship("InterseccionModel", back_populates="linea")


class ParadaModel(Base):
    __tablename__ = 'parada'
    id = Column(Integer, primary_key=True)
    intersecciones = relationship("InterseccionModel", back_populates="parada")
    #paradas = relationship("LineaParadaModel", back_populates="parada")


class CalleModel(Base):
    __tablename__ = 'calle'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    def __str__(self):
        return self.nombre


class InterseccionModel(Base):
    __tablename__ = 'linea_interseccion'
    id_linea = Column(Integer, ForeignKey('linea.id'), primary_key=True)
    id_calle_1 = Column(Integer, ForeignKey('calle.id'))
    id_calle_2 = Column(Integer, ForeignKey('calle.id'))
    id_parada = Column(Integer, ForeignKey('parada.id'), primary_key=True)
    linea = relationship("LineaModel", back_populates='intersecciones')
    parada = relationship("ParadaModel")
    calle_1 = relationship("CalleModel", foreign_keys=[id_calle_1])
    calle_2 = relationship("CalleModel", foreign_keys=[id_calle_2])
    boletos = relationship("BoletoModel")


class BoletoModel(Base):
    __tablename__ = 'boleto'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_linea = Column(Integer)
    id_parada = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (ForeignKeyConstraint([id_linea, id_parada], [InterseccionModel.id_linea, InterseccionModel.id_parada]),)



'''
class LineaParadaModel(Base):
    __tablename__ = 'lineas_paradas'
    linea_id = Column(Integer, ForeignKey('linea.id'), primary_key=True)
    parada_id = Column(Integer, ForeignKey('parada.id'), primary_key=True)
    linea = relationship("LineaModel", back_populates="lineaParadas")
    parada = relationship("ParadaModel", back_populates="paradas")
'''

print(np.random.normal(0, 1, size=(1, 4)))

_DATE_RANGE = ('2020-01-01 00:00:00', '2020-01-02 00:00:00')
_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
_EMPIRICAL_SCALE_RATIO = 0.15
_DISTRIBUTION_SIZE = 1000

time_range = tuple(time.mktime(time.strptime(d, _DATE_FORMAT))
                   for d in _DATE_RANGE)
distribution = np.random.normal(
    loc=(time_range[0] + time_range[1]) * 0.5,
    scale=(time_range[1] - time_range[0]) * _EMPIRICAL_SCALE_RATIO,
    size=_DISTRIBUTION_SIZE
)
date_range = tuple(time.strftime(_DATE_FORMAT, time.localtime(t))
                   for t in np.sort(distribution))
print(date_range) #Acá queda el arreglo de fechas con distribución uniforme

##Gráfica acumulativa de fechas con distribución normal.
pyplot.hist(date2num(date_range), cumulative=True)
pyplot.show()