from app.models.usuario import funcionario, cliente
from app.controllers.database import addinfo, getinfo

#modelo
# pessoa = funcionario(None, 'felipe', 'felipecarrijo19@gmail.com', '04055430183', 'felipe19' )

# pessoa = funcionario(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19', None)
# pessoa2 = adm(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19', None)
# pessoa3 = cliente(None, None, 'felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19')

# addinfo().add_produto_novo('melancia', 7.0, 5.5, 0)
# addinfo().buy_produto(3, 30)
# getinfo().get_all_produtos()

addinfo().add_adm('teste_adm','teste_adm@gmail.com', '04055430183', 'teste_adm')
# addinfo().add_funcionario('felype', 'felypecarrijo19@gmail.com', '04055430183', 'felype19')
