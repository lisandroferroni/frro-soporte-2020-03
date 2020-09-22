import datetime

from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime, ForeignKeyConstraint, Time
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
    id_cuadro = Column(Integer, ForeignKey('cuadro.id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (ForeignKeyConstraint([id_linea, id_parada], [InterseccionModel.id_linea, InterseccionModel.id_parada]),)

class CuadroModel(Base):
    __tablename__ = 'cuadro'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_linea = Column(Integer)
    id_parada = Column(Integer)
    hora = Column(Time)
    tipo_dia = Column(Integer, default=0)
    __table_args__ = (ForeignKeyConstraint([id_linea, id_parada], [InterseccionModel.id_linea, InterseccionModel.id_parada]),)

'''
class LineaParadaModel(Base):
    __tablename__ = 'lineas_paradas'
    linea_id = Column(Integer, ForeignKey('linea.id'), primary_key=True)
    parada_id = Column(Integer, ForeignKey('parada.id'), primary_key=True)
    linea = relationship("LineaModel", back_populates="lineaParadas")
    parada = relationship("ParadaModel", back_populates="paradas")
'''
