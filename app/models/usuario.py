from app.controllers.database import getinfo, addinfo
from app.models.itens import produto


class cliente:
    def __init__(self, seccion_id, trabalhador, nome, email, cpf, senha):
        self.seccion_id = seccion_id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.trabalhador = trabalhador


#=================================================================================
class funcionario(cliente):
    def __init__(self,seccion_id, trabalhador, nome, email, cpf, senha, salario):
        super().__init__(seccion_id, trabalhador, nome, email, cpf, senha)
        self.salario = salario

#---------------------------------------------------------------------------------

    def vender_produto(self, id, qtd):
        existencia = getinfo().get_produtos(id)[0]
        if existencia:
            addinfo().sell_produto(id,qtd)
        else:
            print('Produto nao cadastrado')

    def comprar_produto(self, id, qtd):
        existencia = getinfo().get_produtos(id)[0]
        if existencia:
            addinfo().buy_produto(id,qtd)
        else:
            print('Produto nao cadastrado')
            
    def adicionar_cliente(self, nome, email, cpf, senha):
        addinfo().add_cliente(nome,email,cpf,senha)


#=================================================================================
class adm(funcionario):
    def __init__(self,seccion_id, trabalhador, nome, email, cpf, senha, salario):
        super().__init__(seccion_id, trabalhador,nome, email, cpf, senha, salario)
        
#---------------------------------------------------------------------------------
        
    def adicionar_produto_novo(self, nome, preco_venda, preco_compra, item):
        catalogo = ['Alimentos','Higiene','Limpeza','Outros']
        novo_produto = produto(nome, preco_venda, preco_compra, catalogo[item])
        addinfo().add_produto_novo(novo_produto.nome, novo_produto.preco_venda, novo_produto.preco_compra, novo_produto.categoria)
        
    def adicionar_funcionario(self, nome, email, cpf, senha):
        addinfo().add_funcionario(nome,email,cpf,senha)
        
    def adicionar_adm(self, nome, email, cpf, senha):
        addinfo().add_adm(nome,email,cpf,senha)