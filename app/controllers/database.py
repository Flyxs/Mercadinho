import sqlite3
from datetime import datetime
    
data_atual = datetime.today().strftime('%d-%m-%Y')
hora_atual = datetime.now().strftime('%H:%M:%S')


conexao = sqlite3.connect('app/controllers/db/mercadinho.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_venda REAL NOT NULL,
    preco_compra REAL NOT NULL,
    quantidade INTEGER DEFAULT 0,
    categoria TEXT NOT NULL DEFAULT 'Sem categoria'
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seccion_id TEXT,
    trabalhador BOOLEAN DEFAULT 1,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cpf TEXT NOT NULL,
    senha TEXT NOT NULL,
    salario REAL DEFAULT 1700
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS adms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seccion_id TEXT,
    trabalhador BOOLEAN DEFAULT 2,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cpf TEXT NOT NULL,
    senha TEXT NOT NULL,
    salario REAL DEFAULT 3000
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seccion_id TEXT,
    trabalhador BOOLEAN DEFAULT 0,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cpf TEXT NOT NULL,
    senha TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS saldo (
    despesa REAL DEFAULT 0,
    receita REAL DEFAULT 0,    
    total REAL DEFAULT 1000
);
''')

cursor.execute('SELECT COUNT(*) FROM saldo')
resultado = cursor.fetchone()
if resultado[0] == 0:
    cursor.execute('INSERT INTO saldo (despesa, receita) VALUES (0, 0)')

conexao.commit()
conexao.close()


#===============================================================================================================================
class database:
    def __init__(self):
        self.conexao = sqlite3.connect('app/controllers/db/mercadinho.db')
        self.cursor = self.conexao.cursor()
        
    def close(self):
        self.conexao.close()
        
    def commit(self):
        self.conexao.commit()

#===============================================================================================================================
class getinfo(database):
    def __init__(self):
        super().__init__()
        
    def get_produtos(self,id):
        self.cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        produto = self.cursor.fetchone()
        return produto
    
    def get_funcionario(self,email):
        self.cursor.execute('SELECT * FROM funcionarios WHERE email = ?', (email,))
        usuario = self.cursor.fetchone()
        return usuario
    
    def get_adm(self,email):
        self.cursor.execute('SELECT * FROM adms WHERE email = ?', (email,))
        adm = self.cursor.fetchone()
        return adm
    
    def get_cliente(self,email):
        self.cursor.execute('SELECT * FROM clientes WHERE email = ?', (email,))
        cliente = self.cursor.fetchone()
        return cliente
    
    def get_user(self, email):
        user = None
        self.cursor.execute('SELECT * FROM funcionarios WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        
        if user is None:
            self.cursor.execute('SELECT * FROM adms WHERE email = ?', (email,))
            user = self.cursor.fetchone()
        if user is None:
            self.cursor.execute('SELECT * FROM clientes WHERE email = ?', (email,))
            user = self.cursor.fetchone()
        
        return user
    
    def autenticar(self,email,senha):
        user = self.get_user(email)
        if user[4] == email and user[6] == senha:
            return True
        else:
            return False
     
    
#===============================================================================================================================
class addinfo(database):
    def __init__(self):
        super().__init__()
        
    def add_produto_novo(self,nome,preco_venda,preco_compra,categoria):
        try:
            self.cursor.execute('INSERT INTO produtos (nome, preco_venda, preco_compra, categoria) VALUES (?,?,?,?)',(nome,preco_venda,preco_compra, categoria))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao cadastrar produto')
        
    def add_produto(self,id,quantidade):
        try:
            id = int(id)
            quantidade = int(quantidade)
            self.cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (id,))
            qtd = self.cursor.fetchone()[0]
            qtd = qtd + quantidade
            self.cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?',(qtd,id))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao adicionar produto')
            
    def rm_produto(self,id,quantidade):
        try:
            id = int(id)
            quantidade = int(quantidade)
            self.cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (id,))
            qtd = self.cursor.fetchone()[0]
            qtd = qtd - quantidade
            self.cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?',(qtd,id))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao remover produto')
            
    def buy_produto(self,id,quantidade):
        try:
            self.cursor.execute('SELECT preco_compra FROM produtos WHERE id = ?', (id,))
            preco = self.cursor.fetchone()[0]
            preco = preco * quantidade
            
            self.cursor.execute('SELECT * FROM saldo')
            resultado = self.cursor.fetchone()
            despesa = resultado[0]
            saldo = resultado[2]
            despesa = despesa + preco
            saldo = saldo - preco
            
            self.cursor.execute('INSERT INTO transacoes (data,horario,valor,tipo) VALUES (?,?,?,?)',(data_atual,hora_atual,preco,'Compra'))
            self.cursor.execute('UPDATE saldo SET total = ?, despesa = ? WHERE ROWID = 1', (saldo, despesa))
            
            self.commit()
            self.add_produto(id,quantidade)
            
        except sqlite3.Error as e:
            print('Erro ao comprar produto', e)
            
    def sell_produto(self,id,quantidade):
        try:
            self.rm_produto(id,quantidade)
            self.cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (id,))
            qtd = self.cursor.fetchone()[0]
            if qtd >= 0:
                self.cursor.execute('SELECT preco_venda FROM produtos WHERE id = ?', (id,))
                preco = self.cursor.fetchone()[0]
                preco = preco * quantidade
                
                self.cursor.execute('SELECT * FROM saldo')
                resultado = self.cursor.fetchone()
                receita = resultado[1]
                saldo = resultado[2]
                receita = receita + preco
                saldo = saldo + preco
                
                self.cursor.execute('INSERT INTO transacoes (data,horario,valor,tipo) VALUES (?,?,?,?)',(data_atual,hora_atual,preco,'Venda'))
                self.cursor.execute('UPDATE saldo SET total = ?, receita = ? WHERE ROWID = 1', (saldo, receita))
                
                self.commit()
            else:
                self.add_produto(id,quantidade)
                print('Quantidade insuficiente')
        except sqlite3.Error as e:
            print('Erro ao vender produto', e)
            
        
    def add_funcionario(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO funcionarios (nome, email, cpf, senha) VALUES (?,?,?,?)',(nome,email,cpf,senha))
            self.conexao.commit()

        except sqlite3.OperationalError:
            print('Erro ao cadastrar funcionario')
        
    def add_adm(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO adms (nome, email, cpf, senha) VALUES (?,?,?,?)',(nome,email,cpf,senha))
            self.commit()
            
        except sqlite3.OperationalError:
            print('Erro ao cadastrar adm')
            
    def add_cliente(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO clientes (nome, email, cpf, senha) VALUES (?,?,?,?)',(nome,email,cpf,senha))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao cadastrar cliente')