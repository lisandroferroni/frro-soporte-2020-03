import graphene
from graphene import ObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import *
from data import DatosBoleto
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


class CreateBoleto (graphene.Mutation):
    class Arguments:
        id_linea = graphene.Int()
        id_parada = graphene.Int()

    boleto = graphene.Field(Boleto)

    def mutate (self, info, id_linea, id_parada):
        datosBoleto = DatosBoleto()
        boleto = BoletoModel(id_linea=id_linea, id_parada=id_parada)
        datosBoleto.alta(boleto)
        return CreateBoleto(boleto)


class Mutations(graphene.ObjectType):
    create_boleto = CreateBoleto.Field()


class Query(graphene.ObjectType):
    calles = graphene.List(Calle)
    calleSearch = graphene.List(Calle, q=graphene.String())
    calle1_by_id_linea = graphene.List(Interseccion, idLinea=graphene.Int())
    calle2_by_idLinea_calle1 = graphene.List(Interseccion, idLinea=graphene.Int(), idCalle1=graphene.Int())
    lineas = graphene.List(Linea)
    paradas = graphene.List(Parada)
    parada_by_idlinea_c1_c2 = graphene.List(Interseccion, idLinea=graphene.Int(), idCalle1=graphene.Int(), idCalle2=graphene.Int())
    boleto_by_linea_parada = graphene.List(Boleto, idLinea=graphene.Int(), idParada=graphene.Int(), deltaDias=graphene.Int())
    boletos = graphene.List(Boleto)
    all_calles = SQLAlchemyConnectionField(Calle)
    all_lineas = SQLAlchemyConnectionField(Linea)
    all_paradas = SQLAlchemyConnectionField(Parada)
    linea = graphene.Field(Linea, id = graphene.Int())

    def resolve_calles(self, info):
        query = Calle.get_query(info)  # SQLAlchemy query
        return query.all()

    def resolve_calleSearch(self, info, **args):
        q = args.get("q")  # Search query
        query = Calle.get_query(info)  # SQLAlchemy query
        calles = query.filter(CalleModel.nombre.contains(q)).all()
        return calles

    def resolve_calle1_by_id_linea(self, info, idLinea):
        query = Interseccion.get_query(info)  # SQLAlchemy query
        calles = query.filter(InterseccionModel.id_linea==idLinea).\
            join(CalleModel, CalleModel.id == InterseccionModel.id_calle_1, isouter=True). \
            order_by(CalleModel.nombre). \
            group_by(InterseccionModel.id_calle_1).\
            all()
        return calles

    def resolve_calle2_by_idLinea_calle1(self, info, idLinea, idCalle1):
        query = Interseccion.get_query(info)  # SQLAlchemy query
        calles = query.\
            filter(InterseccionModel.id_calle_1==idCalle1, InterseccionModel.id_linea==idLinea).\
            join(CalleModel, CalleModel.id == InterseccionModel.id_calle_2, isouter=True).\
            order_by(CalleModel.nombre).\
            all()
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
        print(query.statement.compile(compile_kwargs={"literal_binds": True}))
        return query.all()

    def resolve_parada_by_idlinea_c1_c2(self, info, idLinea, idCalle1, idCalle2):
        query = Interseccion.get_query(info)  # SQLAlchemy query
        parada = query.\
            filter(
                InterseccionModel.id_linea == idLinea,
                InterseccionModel.id_calle_1 == idCalle1,
                InterseccionModel.id_calle_2 == idCalle2
            ).\
            all()
        return parada

    def resolve_boleto_by_linea_parada(self, info, idLinea, idParada, deltaDias):
        #weekday = datetime.datetime.today().weekday()
        fecha_ahora = datetime.utcnow()
        fecha_min = fecha_ahora.date() + timedelta(days=-deltaDias)
        boletos = Boleto.get_query(info).filter(
            BoletoModel.id_linea==idLinea,
            BoletoModel.id_parada==idParada,
            BoletoModel.created_date < fecha_ahora,
            BoletoModel.created_date > fecha_min
        ).all()

        print(Boleto.get_query(info).filter(
            BoletoModel.id_linea==idLinea,
            BoletoModel.id_parada==idParada,
            BoletoModel.created_date < fecha_ahora,
            BoletoModel.created_date > fecha_min
        ).statement.compile(compile_kwargs={"literal_binds": True}))
        return boletos


schema = graphene.Schema(query=Query, types=[Linea], mutation=Mutations)

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
