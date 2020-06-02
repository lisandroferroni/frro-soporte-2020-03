from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base, engine

class LineaModel(Base):
    __tablename__ = 'lineas'
    uuid = Column('id', Integer, primary_key=True)
    name = Column('nombre', String(15))
    uuid_entidad = Column('id_entidad', Integer)
    def __str__(self):
        return self.name

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
