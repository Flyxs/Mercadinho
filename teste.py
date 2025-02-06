from app.models.usuario import funcionario, adm
from app.controllers.database import addinfo, getinfo


pessoa = funcionario('felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19' )
pessoa2 = adm('felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19' )

# pessoa2.adicionar_produto_novo('maçã', 7.0, 4.0)

# getinfo().get_produtos(1)

# pessoa2.comprar_produto(1, 5)

pessoa2.vender_produto(1, 3)