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
        print('\n usuario encontrado \n', user)
        
        if not user:
            print('redirecionando para login')
            return redirect('/login')
        
        else:
            if request.method == 'GET':
                print('\n metodo GET encontrado \n')
                produtos = getinfo().get_all_produtos()
                carrinho = getinfo().get_carrinho(user[0])
                print('\n produtos encontrados', produtos)
                print('carrinho encontrado', carrinho, '\n')
                return template('app/views/html/produtos', produtos=produtos, carrinho=carrinho)
            
            elif request.method == 'POST':
                print('\n metodo POST encontrado \n')

                produto_id = request.forms.get('produto_id')
                quantidade = request.forms.get('quantidade')
                print('\n produto_id: ', produto_id)
                print('quantidade: ', quantidade, '\n')
                
                if not produto_id or not quantidade:
                    print('\n campo vazio \n')
                    return redirect('/produtos')
                
                try:
                    quantidade = int(quantidade)
                except ValueError:
                    print('\n quantidade invalida \n')
                    quantidade = 0
                    return redirect('/produtos')
                
                addinfo().add_carrinho(user[0], produto_id, quantidade)
                addinfo().rm_produto(produto_id, quantidade)

                
                return redirect('/produtos')
            
    def carrinho(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')
        
        else:
            carrinho = getinfo().get_carrinho(user[0])
            if request.method == 'GET':
                
                confirmacao = False
                total_carrinho = sum(produto[3] * produto[2] for produto in carrinho)
                
                if not carrinho:
                    mensagem = 'Carrinho vazio'
                else:
                    mensagem = 'Seu carrinho'
                    
                return template('app/views/html/carrinho', carrinho=carrinho, mensagem=mensagem, total=total_carrinho, confirmacao=confirmacao)
            
            elif request.method == 'POST':
                cancelar_carrinho = request.forms.get('cancelar_carrinho')
                
                if cancelar_carrinho:
                    
                    for item in carrinho:
                        addinfo().add_produto(item[0], item[2])  # Reabastece o estoque
                        addinfo().remove_carrinho(user[0], item[0])  # Remove do carrinho
                    return redirect('/produtos')
                
                else:
                    cancelar_produto = request.forms.get('cancelar_produto')
                    
                    if cancelar_produto:
                        qtd = request.forms.get('quantidade')
                        addinfo().add_produto(cancelar_produto, qtd)  # Reabastece o estoque
                        addinfo().remove_carrinho(user[0], cancelar_produto)  # Remove o produto específico
                        return redirect('/carrinho')
                    
                    confirmacao = True
                    for item in carrinho:
                        addinfo().sell_produto(item[0], item[2])  # Confirma a venda
                        addinfo().remove_carrinho(user[0], item[0])  # Remove os produtos do carrinho
                        
                    return template('app/views/html/carrinho', carrinho=[], mensagem="Compra confirmada!", total=0)

