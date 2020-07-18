import datetime
from sqlalchemy import Column, Table, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class CalleModel(Base):
    __tablename__ = 'calle'
    uuid = Column('IdCalle', Integer, primary_key=True)
    name = Column('Nombre', String(100))
    def __str__(self):
        return self.name

lineas_paradas_table = Table('lineas_paradas', Base.metadata,
    Column('linea_id', Integer, ForeignKey('linea.id'), primary_key=True),
    Column('parada_id', Integer, ForeignKey('parada.id'), primary_key=True),
)

''' modelo usado para representar a la asociación y a la tabla, para usar en BoletoModel
class LineaParadaModel(Base):
    __tablename__ = 'lineas_paradas'
    linea_id = Column(Integer, ForeignKey('linea.id'), primary_key=True)
    parada_id = Column(Integer, ForeignKey('parada.id'), primary_key=True)
    parada = relationship("ParadaModel", back_populates="linea")
    linea = relationship("LineaModel", back_populates="parada")
'''

class LineaModel(Base):
    __tablename__ = 'linea'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    paradas = relationship("ParadaModel", secondary=lineas_paradas_table, back_populates="lineas")
    #paradas = relationship("LineaParadaModel", secondary="lineas_paradas")

class ParadaModel(Base):
    __tablename__ = 'parada'
    id = Column(Integer, primary_key=True)
    id_calle_ppal = Column(Integer)
    id_calle_cruce = Column(Integer)
    lineas = relationship("LineaModel", secondary=lineas_paradas_table, back_populates="paradas")
    #lineas = relationship("LineaParadaModel", secondary="lineas_paradas")

class BoletoModel(Base):
    __tablename__ = 'boleto'
    id = Column(Integer, primary_key=True)
    id_linea = Column(Integer, ForeignKey('lineas_paradas.linea_id'))
    id_parada = Column(Integer, ForeignKey('lineas_paradas.parada_id'))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
