from sqlalchemy import Column, Table, Integer, ForeignKey, String
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
    Column('linea_id', Integer, ForeignKey('linea.id')),
    Column('parada_id', Integer, ForeignKey('parada.id'))
)

class LineaModel(Base):
    __tablename__ = 'linea'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    paradas = relationship("ParadaModel", secondary=lineas_paradas_table, back_populates="lineas")

class ParadaModel(Base):
    __tablename__ = 'parada'
    id = Column(Integer, primary_key=True)
    id_calle_ppal = Column(Integer)
    id_calle_cruce = Column(Integer)
    lineas = relationship("LineaModel", secondary=lineas_paradas_table, back_populates="paradas")

##Data
"""
db_session = sessionmaker()
session = db_session()
with open('../1lineas.json') as json_file:
    data = json.load(json_file)
    for l in data['0']:
        print('Name: ' + l['txt']+" "+l['attrs']['idlinea'])
        session.add(LineaModel(uuid=l['attrs']['idlinea'], name=l['txt']))
session.commit()
"""
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
