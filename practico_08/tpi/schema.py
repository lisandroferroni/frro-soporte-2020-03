import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *

class Linea(SQLAlchemyObjectType):
    class Meta:
        model = LineaModel
        interfaces = (graphene.relay.Node,)

class Parada(SQLAlchemyObjectType):
    class Meta:
        model = ParadaModel
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    lineas = graphene.List(Linea)
    paradas = graphene.List(Parada)
    all_lineas = SQLAlchemyConnectionField(Linea)
    all_paradas = SQLAlchemyConnectionField(Parada)
    linea = graphene.Field(Linea, id = graphene.Int())
    def resolve_lineas(self, info):
        query = Linea.get_query(info)  # SQLAlchemy query
        return query.all()
    def resolve_linea(self, info, **args):
        query = Linea.get_query(info)
        id = args.get('id')
        return query.get(id)



schema = graphene.Schema(query=Query, types=[Linea])

'''
class Person(SQLAlchemyObjectType):

    class Meta:
        model = PersonModel
        interfaces = (graphene.relay.Node, )

class Article(SQLAlchemyObjectType):

    class Meta:
        model = ArticleModel
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):

    node = graphene.relay.Node.Field()
    person = graphene.Field(Person, uuid = graphene.Int())

    def resolve_person(self, args, context, info):
        query = Person.get_query(context)
        uuid = args.get('uuid')
        return query.get(uuid)

schema = graphene.Schema(query=Query, types=[Person])
'''
