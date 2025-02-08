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

                addinfo().add_cliente(usuario, email, cpf, senha)
                print('cliente cadastrado com sucesso')
                return template('app/views/html/login', error_message=error_message)
                

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
                        classes = {"cliente": cliente, "funcionario": funcionario, "adm": adm}
                        pessoa_dados = getinfo().get_user(email)
                        pessoa = pessoa_dados[1]
                            

                        print(pessoa_dados)
                        user = classes[pessoa](*pessoa_dados)
                        print(user)
                            
                        if not user:
                            print('erro ao achar o tipo de usuario')
                            error_message = 'Erro ao logar. Tente novamente.'
                            return template('app/views/html/login', error_message=error_message)
                                
                        else:
                            print('0')
                            addinfo().create_session(user.id, pessoa)
                            print('1')
                            if pessoa == 'cliente':
                                return template('app/views/html/dashboard_c', nome = user.nome)
                            elif pessoa == 'funcionario' or pessoa == 'adm':
                                return template('app/views/html/dashboard_f', nome = user.nome)

                                
        except Exception as e:
            print('Erro ao logar:', e)
            error_message = 'Erro ao logar. Tente novamente.'                
            return template('app/views/html/login', error_message=error_message)


    def logout(self):
        session_id = request.get_cookie('session_id')
        print(session_id)
        if session_id:
            addinfo().delete_session(session_id)
            response.delete_cookie('session_id')
            
        return template('app/views/html/index')


    def dashboard_c(self):
        user = getinfo().check_session()
        if user:
            return template('app/views/html/dashboard_c', id = user[0], user_type = user[1], nome = user[2], email = user[3], cpf = user[4], senha = user[5])
        else:
            return template('app/views/html/index')
        

    def dashboard_f(self):
        user = getinfo().check_session()
        if user:
            return template('app/views/html/dashboard_f', id = user[0], user_type = user[1], nome = user[2], email = user[3], cpf = user[4], senha = user[5], salario = user[6])
        else:
            return template('app/views/html/index')
