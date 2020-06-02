import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *

class Linea(SQLAlchemyObjectType):
    class Meta:
        model = LineaModel

class Query(graphene.ObjectType):
    lineas = graphene.List(Linea)
    def resolve_lineas(self, info):
        query = Linea.get_query(info)  # SQLAlchemy query
        return query.all()

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
