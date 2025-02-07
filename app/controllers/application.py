from bottle import template, request, redirect, response
from app.models.usuario import adm, funcionario, cliente
from app.controllers.database import addinfo, getinfo

class Application():

    def __init__(self):
        self.pages = {
            'index': self.index,
            'cadastro': self.cadastro,
            'login': self.login
        }
        

#===================================================================================
    def render(self,page,**kwargs):
       content = self.pages.get(page, self.helper)
       return content(**kwargs)

    def helper(self):
        return template('app/views/html/helper')
    
#===================================================================================

    def index(self):
        return template('app/views/html/index')

    def cadastro(self):
        try:
            error_message = ''
            if request.method == 'GET':
                return template('app/views/html/cadastro', error_message=error_message)
            elif request.method == 'POST':
                usuario = request.forms.get('nome')
                senha = request.forms.get('senha')
                email = request.forms.get('email')
                cpf = request.forms.get('cpf')
                print(usuario, senha, email, cpf)
                if not usuario or not senha or not email or not cpf:
                    error_message = 'Preencha todos os campos'
                    return template('app/views/html/cadastro', error_message=error_message)
                if getinfo().get_cliente(email):
                    error_message = 'Email já cadastrado'
                    return template('app/views/html/cadastro', error_message=error_message)

                else:
                    addinfo().add_cliente(usuario, email, cpf, senha)
                    print('cliente cadastrado com sucesso')
                    return template('app/views/html/login')
                

        except Exception as e:
            print('Erro ao cadastrar', e)
            error_message = 'Erro ao cadastrar. Tente novamente.'
            return template('app/views/html/cadastro', error_message=error_message)


    def login(self):
        try:
            error_message = ''
            if request.method == 'GET':
                return template('app/views/html/login', error_message=error_message)
            
            elif request.method == 'POST':
                email = request.forms.get('email')
                password = request.forms.get('senha')
                
                if not email or not password:
                    error_message = 'Preencha todos os campos'
                    return template('app/views/html/login', error_message=error_message)
                
                else:
                    if not getinfo().get_user(email):
                        error_message = 'Email nao cadastrado'
                        return template('app/views/html/login', error_message=error_message)
                    
                    elif not getinfo().autenticar(email, password):
                        print('usuario não autenticado')
                        error_message = 'Email ou senha incorretos'
                        return template('app/views/html/login', error_message=error_message)
                    
                    else:
                        classes = {0: cliente, 1: funcionario, 2: adm}
                        pessoa_dados = getinfo().get_user(email)
                        pessoa = pessoa_dados[2]
                        
                        print(pessoa_dados)
                        user = classes[pessoa](*pessoa_dados[1:])
                        print(user)
                        
                        if not user:
                            print('erro ao achar o tipo de usuario')
                            error_message = 'Erro ao logar. Tente novamente.'
                            return template('app/views/html/login', error_message=error_message)
                            
                        else:
                            response.set_cookie('session_id', str(user.seccion_id), httponly=True, secure=True, max_age=3600)
                            if pessoa == 0:
                                return template('app/views/html/dashboard_c', nome = user.nome)
                            elif pessoa == 1 or pessoa == 2:
                                return template('app/views/html/dashboard_f', nome = user.nome)

                            
        except Exception as e:
            print('Erro ao logar:', e)
            error_message = 'Erro ao logar. Tente novamente.'
            return template('app/views/html/login', error_message=error_message)
        
        
    def logout(self):
        response.delete_cookie('session_id')
        return template('app/views/html/index')
    
    