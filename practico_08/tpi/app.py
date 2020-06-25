from flask import Flask, render_template

from database import db_session
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True
app.env = 'development'
app.templates_auto_reload = True

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, context={'session': db_session}))

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
    return render_template('lineas.html')

if __name__ == '__main__':
    app.run()
