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
            'vendas': self.vendas,
            'usuarios': self.usuarios
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
                    if pessoa == 'adm':
                        pessoa = 'funcionario'
                        

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
            print('logout efetuado')
            
        return redirect('/')



    def dashboard_c(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')            

        else:
            carrinho = getinfo().get_carrinho(user[0])
            print('carrinho encontrado', carrinho, '\n')
            
            if request.method == 'GET':

                total_carrinho = sum(produto[3] * produto[2] for produto in carrinho)
                
                if not carrinho:
                    mensagem = 'Carrinho vazio'
                else:
                    mensagem = 'Seu carrinho'
                    
                return template('app/views/html/dashboard_c', user=user, carrinho=carrinho, mensagem=mensagem, total=total_carrinho)

            
            elif request.method == 'POST':
                
                cancelar_carrinho = request.forms.get('cancelar_carrinho')
                
                if cancelar_carrinho:
                    
                    for item in carrinho:
                        addinfo().add_produto(item[0], item[2])  # Reabastece o estoque
                        addinfo().remove_carrinho(user[0], item[0])  # Remove do carrinho
                    return redirect('/dashboard_c')
                
                else:
                    cancelar_produto = request.forms.get('cancelar_produto')
                    
                    if cancelar_produto:
                        qtd = request.forms.get('quantidade')
                        addinfo().add_produto(cancelar_produto, qtd)  # Reabastece o estoque
                        addinfo().remove_carrinho(user[0], cancelar_produto)  # Remove o produto específico
                        return redirect('/dashboard_c')
                    
                    confirmar_compra = request.forms.get('confirmar_compra')
                    
                    if confirmar_compra:
                        for item in carrinho:
                            addinfo().sell_produto(item[0], item[2])  # Confirma a venda
                            addinfo().remove_carrinho(user[0], item[0])  # Remove os produtos do carrinho
                        
                        return redirect('/dashboard_c')   

        
    def dashboard_f(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')
        
        else:
            if user[1] == 'funcionario' or user[1] == 'adm':
                if request.method == 'GET':
                    return template('app/views/html/dashboard_f', user=user)
                elif request.method == 'POST':
                    return template('app/views/html/dashboard_f', user=user)       
            else:
                return redirect('/dashboard_c')     
            


    def produtos(self):
        user = getinfo().check_session()
        print('\n usuario encontrado \n', user)
        
        if not user:
            print('redirecionando para login')
            return redirect('/login')
        
        else:
            produto_id = request.forms.get('produto_id')
            quantidade = request.forms.get('quantidade')            
            produtos = getinfo().get_all_produtos()
            
            if user[1] == 'cliente':
                if request.method == 'GET':
                    print('\n metodo GET encontrado \n')
                    carrinho = getinfo().get_carrinho(user[0])
                    print('\n produtos encontrados', produtos)
                    print('carrinho encontrado', carrinho, '\n')
                    return template('app/views/html/produtos', produtos=produtos, carrinho=carrinho, user=user)
                
                elif request.method == 'POST':
                    print('\n metodo POST encontrado \n')


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
                
                    
            elif user[1] == 'funcionario' or user[1] == 'adm':
                if request.method == 'GET':
                    
                    return template('app/views/html/produtos', produtos=produtos, user=user)
                
                elif request.method == 'POST':
                    
                    produto_id = request.forms.get('produto_id')
                    nome = request.forms.get('nome_produto')
                    excluir = request.forms.get('excluir_produto')  
                                      
                    print('\nproduto_id: ', produto_id)
                    print('quantidade: ', quantidade)
                    print('nome: ', nome)
                    print('excluir: ', excluir, '\n')
                    
                  
                    if produto_id:
                        
                        quantidade = request.forms.get('quantidade')
                        try:
                            quantidade = int(quantidade)
                        except ValueError:
                            print('\n quantidade invalida \n')
                            quantidade = 0
                            return redirect('/produtos')                        
                        
                        addinfo().buy_produto(produto_id, quantidade)
                        

                    elif nome:
                        print('adicionando produto')
                        preco_compra = float(request.forms.get('preco_compra'))
                        print('preco_compra: ',preco_compra)
                        preco_venda = float(request.forms.get('preco_venda'))
                        print('preco_venda: ',preco_venda)
                        categoria = int(request.forms.get('tipo'))
                        print('categoria: ',categoria)
                        
                        
                        if nome and preco_compra and preco_venda:
                            print('adicionando produto')
                            addinfo().add_produto_novo(nome, preco_venda, preco_compra, categoria)
                            print('produto adicionado')
                        
                    elif excluir:
                        addinfo().del_produto(excluir)
                    
                    return redirect('/produtos')
                    

    def vendas(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')
        
        else:
            if user[1] == 'cliente':
                return redirect('/dashboard_c')
            
            else:
                if request.method == 'GET':
                    trasacoes = getinfo().get_transacoes()
                    saldo = getinfo().get_saldo()
                    return template('app/views/html/vendas', transacoes=trasacoes, user=user, saldo=saldo)

                    
    def usuarios(self):
        user = getinfo().check_session()
        if not user:
            return redirect('/login')
        
        if user[1] == 'cliente':
            return redirect('/dashboard_c')

        clientes = getinfo().get_all_clientes()
        funcionarios = getinfo().get_all_funcionarios()

        if request.method == 'GET':
            return template('app/views/html/usuarios', clientes=clientes, funcionarios=funcionarios, user=user, show_cliente=None, show_funcionario=None)

        elif request.method == 'POST':
            show_cliente = request.forms.get('show_cliente')
            show_funcionario = request.forms.get('show_funcionario')
            
            if show_cliente or show_funcionario:
                return template('app/views/html/usuarios', clientes=clientes, funcionarios=funcionarios, user=user, show_cliente=show_cliente if show_cliente else None, show_funcionario=show_funcionario if show_funcionario else None)

            excluir = request.forms.get('excluir')
            if excluir:
                addinfo().remove_user(excluir)
                return template('app/views/html/usuarios', clientes=clientes, funcionarios=funcionarios, user=user, show_cliente=show_cliente if show_cliente else None, show_funcionario=show_funcionario if show_funcionario else None)
            
            promover = request.forms.get('promover')
            if promover:
                addinfo().promover_user(promover)
                return template('app/views/html/usuarios', clientes=clientes, funcionarios=funcionarios, user=user, show_cliente=show_cliente if show_cliente else None, show_funcionario=show_funcionario if show_funcionario else None)
            
            rebaixar = request.forms.get('rebaixar')
            if rebaixar:
                addinfo().rebaixar_user(rebaixar)
                return template('app/views/html/usuarios', clientes=clientes, funcionarios=funcionarios, user=user, show_cliente=show_cliente if show_cliente else None, show_funcionario=show_funcionario if show_funcionario else None)
            
            
            return redirect('/usuarios')
            

                    

