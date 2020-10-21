from flask import Flask, render_template, request

from negocio import StoredProcedureNegocio
from data import db_session
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True
app.env = 'development'
app.templates_auto_reload = True

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, get_context=lambda: {'session': db_session}))


@app.route('/cuandoLlego')
def cuandoLlego():
   deltaDias  = request.args.get('deltaDias', None)
   fecha  = request.args.get('fecha', None)
   linea  = request.args.get('linea', None)
   parada  = request.args.get('parada', None)
   spNegocio = StoredProcedureNegocio()
   return str(spNegocio.cuandoLlego(deltaDias, fecha, linea, parada))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def r_home():
    return render_template('home.html')


@app.route('/paradas-de-colectivo')
def r_paradas_de_colectivo():
    return render_template('paradas-de-colectivo.html')


@app.route('/lineas')
def r_lineas():
    return render_template('cuadros-de-horario.html')

@app.route('/boletos')
def r_boletos():
    return render_template('boletos.html')


if __name__ == '__main__':
    app.run()

# [X] Selector linea y selector parada en Cuadro de Horarios
# [X] Gráfico boletos por meses
# [X] Agregar atributo tipo_boleto (Medio boleto / Diferencial o Monedas / Normal / Jubilado)
# [X] Gráfico tipos de boleto en últimos 30 días
# [] Cantidad de boletos en cada parada de una línea en algún día (u hoy)
# [] Gráfico en 24 horas de un día de una línea en una parada
# [X] Agregar atributo género ¿¿¿ a los boletos para algunas tarjetas (las personalizadas)
# [X] Gráfico proporción boletos por género de día
# [X] Gráfico proporción boletos por género de noche
# [] Paradas con más boletos
# [] Línea con más boletos
# [X] Gráfico porcentaje día vs noche por boletos gral.
# [X] Borrar text Cuando llegó
# [X] Cuadro horario fix time format.
# [] Agregar diagrama de la base al informe.
# [] Número de parada incorrecto