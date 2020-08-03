import graphene
from graphene import ObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *
from datetime import datetime, timedelta

class Linea(SQLAlchemyObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = LineaModel
        interfaces = (graphene.relay.Node,)


class Parada(SQLAlchemyObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = ParadaModel
        interfaces = (graphene.relay.Node, )


class Calle(SQLAlchemyObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = CalleModel
        interfaces = (graphene.relay.Node, )


class Interseccion(SQLAlchemyObjectType):
    class Meta:
        model = InterseccionModel
        interfaces = (graphene.relay.Node, )


class Boleto(SQLAlchemyObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = BoletoModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    calles = graphene.List(Calle)
    calles = graphene.List(Calle, q=graphene.String())
    calleSearch = graphene.List(Calle, q=graphene.String())
    interSearch = graphene.List(Interseccion, q=graphene.String())
    lineas = graphene.List(Linea)
    paradas = graphene.List(Parada)
    boleto_by_linea_parada = graphene.List(Boleto, idLinea=graphene.Int(), idParada=graphene.Int())
    boletos = graphene.List(Boleto)
    all_calles = SQLAlchemyConnectionField(Calle)
    all_lineas = SQLAlchemyConnectionField(Linea)
    all_paradas = SQLAlchemyConnectionField(Parada)
    linea = graphene.Field(Linea, id = graphene.Int())


    def resolve_calleSearch(self, info, **args):
        q = args.get("q")  # Search query
        query = Calle.get_query(info)  # SQLAlchemy query
        calles = query.filter(CalleModel.nombre.contains(q)).all()
        return calles


    def resolve_interSearch(self, info, **args):
        q = args.get("q")  # Search query
        query = Interseccion.get_query(info)  # SQLAlchemy query
        calles = query.filter(InterseccionModel.id_calle_1==q).join(CalleModel, CalleModel.id == InterseccionModel.id_calle_2, isouter=True).all()
        return calles


    def resolve_lineas(self, info):
        query = Linea.get_query(info)  # SQLAlchemy query
        return query.all()


    def resolve_linea(self, info, **args):
        query = Linea.get_query(info)
        id = args.get('id')
        return query.get(id)


    def resolve_boletos(self, info):
        query = Boleto.get_query(info)  # SQLAlchemy query
        return query.all()


    def resolve_boleto_by_linea_parada(self, info, idLinea, idParada):
        query = Boleto.get_query(info)
        #weekday = datetime.datetime.today().weekday()
        fecha_ahora = datetime.utcnow()
        fecha_min = fecha_ahora + timedelta(days=-7)
        return query.filter(
            BoletoModel.id_linea==idLinea,
            BoletoModel.id_parada==idParada,
            BoletoModel.created_date < fecha_ahora,
            BoletoModel.created_date > fecha_min
        ).all()


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
