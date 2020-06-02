from sqlalchemy import Column, Table, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, backref, sessionmaker
from database import Base, engine
from sqlalchemy.ext.declarative import declarative_base

class CalleModel(Base):
    __tablename__ = 'calle'
    uuid = Column('IdCalle', Integer, primary_key=True)
    name = Column('Nombre', String(15))
    def __str__(self):
        return self.name

class LineaModel(Base):
    __tablename__ = 'linea'
    uuid = Column('IdLinea', Integer, primary_key=True)
    name = Column('Nombre', String(15))
    paradas = relationship("ParadaModel", secondary="lineaparada", back_populates="lineas")

class ParadaModel(Base):
    __tablename__ = 'parada'
    uuid = Column('IdParada', Integer, primary_key=True)
    id_calle_ppal = Column('IdCallePpal', Integer)
    id_calle_cruce = Column('IdCalleCruce', Integer)
    lineas = relationship("LineaModel", secondary="lineaparada", back_populates="paradas")

class LineaParada(Base):
    __tablename__ = 'lineaparada'
    id_linea = Column('IdLinea', Integer, ForeignKey('linea.IdLinea'), primary_key=True)
    id_parada = Column('IdParada', Integer, ForeignKey('parada.IdParada'), primary_key=True)
    #linea = relationship(LineaModel, backref=backref("LineaParadas", cascade="all, delete-orphan"))
    #parada = relationship(ParadaModel, backref=backref("LineaParadas", cascade="all, delete-orphan"))

##Data
'''
c1 = CalleModel(uuid = 1, name = "Santa Fe")
c2 = CalleModel(uuid = 2, name = "Oroño")

p1 = ParadaModel(uuid = 1, id_calle_ppal = 1, id_calle_cruce = 2)

l1 = LineaModel(uuid = 1, name = "115")

l1.Paradas.
p1.Lineas.append(l1)

Session = sessionmaker(bind=engine)
session = Session()
session.add(c1)
session.add(c2)
session.add(p1)
session.add(l1)
session.commit()
'''

'''
class PersonModel(Base):
    __tablename__ = 'person'
    uuid = Column(Integer, primary_key=True)
    Articles = relationship("ArticleModel")

class ArticleModel(Base):
    __tablename__ = 'article'
    uuid = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey("person.uuid"))
'''
Base.prepare(engine)
