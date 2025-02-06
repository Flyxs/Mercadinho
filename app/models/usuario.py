from app.controllers.database import getinfo, addinfo
from app.models.itens import produto

class funcionario:
    def __init__(self, nome, email, cpf, senha):
        self.nome = nome
        self.email = email
        self.__senha = senha
        self.cpf = cpf
        
#---------------------------------------------------------------------------------

    def vender_produto(self, id, qtd):
        existencia = getinfo().get_produtos(id)[0][0]
        if existencia:
            addinfo().sell_produto(id,qtd)
        else:
            print('Produto nao cadastrado')

    def comprar_produto(self, id, qtd):
        existencia = getinfo().get_produtos(id)[0][0]
        if existencia:
            addinfo().buy_produto(id,qtd)
        else:
            print('Produto nao cadastrado')


#=================================================================================
class adm(funcionario):
    def __init__(self, nome, email, cpf, senha):
        super().__init__(nome, email, cpf, senha)
        
#---------------------------------------------------------------------------------
        
    def adicionar_produto_novo(self, nome, preco_venda, preco_compra):
        novo_produto = produto(nome, preco_venda, preco_compra)
        addinfo().add_produto_novo(novo_produto.nome,novo_produto.preco_venda,novo_produto.preco_compra)

