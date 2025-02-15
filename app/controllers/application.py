from bottle import template, request, redirect, response
from app.models.usuario import funcionario, cliente
from app.controllers.database import addinfo, getinfo

class Application():

    def __init__(self):
        self.pages = {
            'index': self.index,
            'cadastro': self.cadastro,
            'login': self.login,
            'dashboard_c': self.dashboard_c,
            'dashboard_f': self.dashboard_f,
            'produtos': self.produtos,
            'carrinho': self.carrinho
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
            return redirect('/login')
                


    def login(self):
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
                    classes = {"cliente": cliente, "funcionario": funcionario}
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
                            return redirect('/dashboard_c')
                        elif pessoa == 'funcionario' or pessoa == 'adm':
                            return redirect('/dashboard_f')



    def logout(self):
        session_id = request.get_cookie('session_id')
        print(session_id)
        if session_id:
            addinfo().delete_session(session_id)
            response.delete_cookie('session_id')
            
        return redirect('/')


    def dashboard_c(self):
        user = getinfo().check_session()
        if user:
            if request.method == 'GET':
                return template('app/views/html/dashboard_c', user=user)
            elif request.method == 'POST':
                return template('app/views/html/dashboard_c', user=user)
        else:
            return redirect('/login')
        

    def dashboard_f(self):
        user = getinfo().check_session()
        if user:
            if request.method == 'GET':
                return template('app/views/html/dashboard_f', user=user)
            elif request.method == 'POST':
                return template('app/views/html/dashboard_f', user=user)
        else:
            return redirect('/login')

    def produtos(self):
        user = getinfo().check_session()
        print('usuario encontrado')
        
        if not user:
            print('redirecionando para login')
            return redirect('/login')
        
        else:
            carrinho = []
            if request.method == 'GET':
                print('metodo encontrado')
                produtos = getinfo().get_all_produtos()
                print('produtos encontrados')
                return template('app/views/html/produtos', produtos=produtos)
            
            elif request.method == 'POST':
                print('post encontrado')

                produto_id = request.forms.get('produto_id')
                quantidade = int(request.forms.get('quantidade'))
                
                carrinho.append({'produto_id': produto_id, 'quantidade': quantidade})   
                             
                for info in carrinho:
                    addinfo().rm_produto(info['produto_id'], info['quantidade'])

                print(carrinho)
                
                return redirect('/produtos')
            
    def carrinho(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')