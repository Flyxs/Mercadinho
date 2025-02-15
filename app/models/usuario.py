class cliente:
    def __init__(self, id, trabalhador, nome, email, cpf, senha):
        self.id = id
        self.trabalhador = trabalhador        
        self.nome = nome
        self.email = email
        self.cpf = cpf        
        self.senha = senha



#=================================================================================
class funcionario(cliente):
    def __init__(self, id, trabalhador, nome, email, cpf, senha, salario):
        super().__init__(id, trabalhador, nome, email, cpf, senha)
        self.salario = salario

