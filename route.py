import eventlet
from eventlet import wsgi
import socketio
from app.controllers.application import Application
from route_websocket import sio  # Importando WebSocket separado
from bottle import Bottle, route, run, request, static_file, redirect, template, response

app = Bottle()
ctl = Application()

combined_app = socketio.WSGIApp(sio, app)

#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')

#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/', method=['GET'])
def index():
    return ctl.render('index')

@app.route('/cadastro', method=['GET', 'POST'])
def cadastro():
    response = ctl.cadastro()
    return ctl.render('cadastro')

@app.route('/login', method=['GET', 'POST'])
def login():
    return ctl.render('login')

@app.route('/logout', method='POST')
def logout():
    return ctl.logout()

@app.route('/dashboard_c', method=['GET', 'POST'])
def dashboard_c():
    return ctl.render('dashboard_c')

@app.route('/dashboard_f', method=['GET', 'POST'])
def dashboard_f():
    return ctl.render('dashboard_f')

@app.route('/produtos', method=['GET', 'POST'])
def produtos():
    return ctl.render('produtos')

@app.route('/vendas', method=['GET', 'POST'])
def vendas():
    return ctl.render('vendas')

@app.route('/usuarios', method=['GET', 'POST'])
def usuarios():
    return ctl.render('usuarios')

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    wsgi.server(eventlet.listen(('0.0.0.0', 8080)), combined_app)