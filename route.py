from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


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


@app.route('/carrinho', method=['GET', 'POST'])
def carrinho():
    return ctl.render('carrinho')


@app.route('/vendas', method=['GET', 'POST'])
def vendas():
    return ctl.render('vendas')


@app.route('/usuarios', method=['GET', 'POST'])
def usuarios():
    return ctl.render('usuarios')







#-----------------------------------------------------------------------------

if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
