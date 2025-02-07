from app.models.usuario import funcionario, adm, cliente
from app.controllers.database import addinfo, getinfo

#modelo
#pessoa = funcionario(None, 'felipe', 'felipecarrijo19@gmail.com', '04055430183', 'felipe19' )

pessoa = funcionario(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19', None)
pessoa2 = adm(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19', None)
pessoa3 = cliente(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19')

pessoa2.adicionar_produto_novo('melancia', 6.0, 3.0, 0)

# getinfo().get_produtos(1)

# pessoa2.comprar_produto(1, 5)

# pessoa2.vender_produto(1, 4)

pessoa2.adicionar_funcionario(pessoa.nome, pessoa.email, pessoa.cpf, pessoa.senha)

pessoa2.adicionar_adm(pessoa2.nome, pessoa2.email, pessoa2.cpf, pessoa2.senha)

pessoa2.adicionar_cliente(pessoa3.nome, pessoa3.email, pessoa3.cpf, pessoa3.senha)