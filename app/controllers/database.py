import sqlite3
from datetime import datetime, timedelta
import uuid
from bottle import response, request
    
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
    user_type TEXT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    cpf TEXT NOT NULL,
    senha TEXT NOT NULL,
    salario REAL DEFAULT 0.0
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type TEXT DEFAULT "cliente",
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


cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_type TEXT NOT NULL,
    session_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS carrinhos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    FOREIGN KEY (user_id) REFERENCES clientes (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);
''')

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
        
#------------------------------------{Area de produtos}------------------------------------#        
        
    def get_produtos(self,id):
        self.cursor.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        produto = self.cursor.fetchone()
        return produto
    
    def get_all_produtos(self):
        try:
            self.cursor.execute('SELECT * FROM produtos')
            produtos = self.cursor.fetchall()
            print(produtos)
            return produtos if produtos else []
        except Exception as e:
            print('Erro ao buscar produtos:', e) 
            return []
    
    def get_transacoes(self):
        try:
            self.cursor.execute('SELECT * FROM transacoes')
            transacoes = self.cursor.fetchall()
            return transacoes if transacoes else []
        except Exception as e:
            print('Erro ao buscar transações:', e) 
            return []
        
    def get_saldo(self):
        try:
            self.cursor.execute('SELECT * FROM saldo')
            saldo = self.cursor.fetchone()
            return saldo
        except Exception as e:
            print('Erro ao buscar saldo:', e) 
            return []
    
#------------------------------------{Area de usuario}------------------------------------#
    
    def get_funcionario(self,email):
        self.cursor.execute('SELECT * FROM funcionarios WHERE email = ?', (email,))
        usuario = self.cursor.fetchone()
        return usuario
    
    def get_all_funcionarios(self):
        try:
            self.cursor.execute('SELECT * FROM funcionarios')
            funcionarios = self.cursor.fetchall()
            return funcionarios if funcionarios else []
        except Exception as e:
            print('Erro ao buscar funcionarios:', e) 
            return []
    
    
    def get_cliente(self,email):
        self.cursor.execute('SELECT * FROM clientes WHERE email = ?', (email,))
        cliente = self.cursor.fetchone()
        return cliente
    
    def get_all_clientes(self):
        try:
            self.cursor.execute('SELECT * FROM clientes')
            clientes = self.cursor.fetchall()
            return clientes if clientes else []
        except Exception as e:
            print('Erro ao buscar clientes:', e) 
            return []
    
    
    def get_user(self, email):
        user = None
        self.cursor.execute('SELECT * FROM funcionarios WHERE email = ?', (email,))
        user = self.cursor.fetchone()
        
        if user is None:
            self.cursor.execute('SELECT * FROM clientes WHERE email = ?', (email,))
            user = self.cursor.fetchone()
        
        return user
    
    
    def autenticar(self,email,senha):
        user = self.get_user(email)
        if user[3] == email and user[5] == senha:
            return True
        else:
            return False
    
#------------------------------------{Area de carrinho}------------------------------------#
    
    def get_carrinho(self,user_id):
        try:
            self.cursor.execute('''
            SELECT c.produto_id, p.nome, c.quantidade, p.preco_venda FROM carrinhos c JOIN produtos p ON c.produto_id = p.id WHERE c.user_id = ?
            ''', (user_id,))
            carrinho = self.cursor.fetchall()
            return carrinho if carrinho else []
            
        except Exception as e:
            print('Erro ao buscar carrinho:', e) 
            return []

    
#------------------------------------{Area de cookie}------------------------------------#

    def check_session(self):
        try:
            session_id = request.get_cookie('session_id')
            if not session_id:
                return None

            session = getinfo().get_session(session_id)
            if session and session['expires_at'] > datetime.now():
                user = getinfo().get_user_from_session_id(session_id)
                return user

            else:
                addinfo().delete_session(session_id)
                return None
        except sqlite3.OperationalError as e:
            print('Erro ao verificar sessão:', e)
            return None
        

    def get_session(self, session_id):
        try:
            self.cursor.execute("SELECT user_id, user_type, expires_at FROM sessions WHERE session_id = ?", (session_id,))
            session = self.cursor.fetchone()

            if session:
                return {
                    'user_id': session[0],
                    'user_type': session[1],
                    'expires_at': datetime.strptime(session[2], "%Y-%m-%d %H:%M:%S")
                }
            return None
        except sqlite3.OperationalError as e:
            print('Erro ao verificar sessão:', e)
            return None


    def get_user_from_session_id(self, session_id):
        try:
            self.cursor.execute("SELECT user_id, user_type FROM sessions WHERE session_id = ?", (session_id,))
            user_id = self.cursor.fetchone()
            
            if user_id:
                if user_id[1] == 'cliente':
                    self.cursor.execute('SELECT * FROM clientes WHERE id = ?', (user_id[0],))
                    user = self.cursor.fetchone()
                    if user:
                        return user
                elif user_id[1] == 'funcionario':
                    self.cursor.execute('SELECT * FROM funcionarios WHERE id = ?', (user_id[0],))
                    user = self.cursor.fetchone()
                    return user
        except sqlite3.OperationalError as e:
            print('Erro ao verificar sessão:', e)
            return None


  
#===============================================================================================================================
class addinfo(database):
    def __init__(self):
        super().__init__()
        
#------------------------------------{Area de produtos}------------------------------------#
        
    def add_produto_novo(self,nome,preco_venda,preco_compra,categoria):
        try:
            catalogo = ['Alimento', 'Limpesa', 'Saude', 'Ferramentas', 'Eletronicos', 'Outros']
            categoria = int(categoria)
            self.cursor.execute('INSERT INTO produtos (nome, preco_venda, preco_compra, categoria) VALUES (?,?,?,?)',(nome,preco_venda,preco_compra, catalogo[categoria]))
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
            if quantidade > 0:
                self.cursor.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?', (quantidade, id))
                self.commit()
        except sqlite3.OperationalError:
            print('Erro ao remover produto')
            
    def del_produto(self,id):
        try:
            self.cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao deletar produto')
            
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
            
        except sqlite3.Error as e:
            print('Erro ao vender produto', e)
                 
#------------------------------------{Area de usuario}------------------------------------#
                 
    def add_funcionario(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO funcionarios (user_type, nome, email, cpf, senha) VALUES (?,?,?,?,?)',('funcionario',nome,email,cpf,senha))
            self.conexao.commit()

        except sqlite3.OperationalError as e:
            print('Erro ao cadastrar funcionario', e)
        
        
    def add_adm(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO funcionarios (user_type, nome, email, cpf, senha) VALUES (?,?,?,?,?)',('adm',nome,email,cpf,senha))
            self.commit()
            
        except sqlite3.OperationalError as e:
            print('Erro ao cadastrar adm', e)
            
            
    def add_cliente(self,nome,email,cpf,senha):
        try:
            self.cursor.execute('INSERT INTO clientes (nome, email, cpf, senha) VALUES (?,?,?,?)',(nome,email,cpf,senha))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao cadastrar cliente')
            
            
    def remove_user(self, email):
        try:
            cliente = getinfo().get_cliente(email)
            
            if cliente:
                self.cursor.execute('DELETE FROM clientes WHERE email = ?', (email,))
                self.commit()
                print(f'Cliente com email {email} removido com sucesso.')
            else:
                funcionario = getinfo().get_funcionario(email)
                if funcionario:
                    self.cursor.execute('DELETE FROM funcionarios WHERE email = ?', (email,))
                    self.commit()
                    print(f'Funcionário com email {email} removido com sucesso.')
                else:
                    print(f'Usuário com email {email} não encontrado em clientes nem em funcionários.')

        except sqlite3.OperationalError as e:
            print(f'Erro ao remover usuário: {e}')


    def promover_user(self, email):
        try:
            user = getinfo().get_user(email)
            if user:
                if user[1] == 'cliente':
                    self.cursor.execute('DELETE FROM clientes WHERE email = ?', (email,))
                    self.cursor.execute('INSERT INTO funcionarios (user_type, nome, email, cpf, senha) VALUES (?,?,?,?,?)',('funcionario',user[2],user[3],user[4],user[5]))
                    self.commit()
                    print(f'Usuário com email {email} promovido para funcionário com sucesso.')
                elif user[1] == 'funcionario':
                    self.cursor.execute('UPDATE funcionarios SET user_type = "adm" WHERE email = ?', (email,))
                    self.commit()
                    print(f'Usuário com email {email} promovido para administrador com sucesso.')
        except sqlite3.OperationalError as e:
            print(f'Erro ao promover usuário: {e}')
    
    def rebaixar_user(self, email):
        try:
            user = getinfo().get_user(email)
            if user:
                if user[1] == 'funcionario':
                    self.cursor.execute('DELETE FROM funcionarios WHERE email = ?', (email,))
                    self.cursor.execute('INSERT INTO clientes (user_type, nome, email, cpf, senha) VALUES (?,?,?,?,?)',('cliente',user[2],user[3],user[4],user[5]))
                    self.commit()
                    print(f'Usuário com email {email} rebaixado para cliente com sucesso.')
                elif user[1] == 'adm':
                    self.cursor.execute('UPDATE funcionarios SET user_type = "funcionario" WHERE email = ?', (email,))
                    self.commit()
                    print(f'Usuário com email {email} rebaixado para funcionário com sucesso.')
        except sqlite3.OperationalError as e:
            print(f'Erro ao rebaixar usuário: {e}')

#------------------------------------{Area de carrinho}------------------------------------#
    
    def add_carrinho(self,user_id,produto_id,quantidade):
        try:
            self.cursor.execute('SELECT id, quantidade FROM carrinhos WHERE user_id = ? AND produto_id = ?', (user_id,produto_id))
            carrinho = self.cursor.fetchone()
            if carrinho:
                nova_qtd = carrinho[1] + quantidade
                self.cursor.execute('UPDATE carrinhos SET quantidade = ? WHERE id = ?', (nova_qtd,carrinho[0]))
            else:
                self.cursor.execute('INSERT INTO carrinhos (user_id, produto_id, quantidade) VALUES (?,?,?)', (user_id,produto_id,quantidade))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao adicionar produto ao carrinho')
            
    def remove_carrinho(self,user_id,produto_id):
        try:
            self.cursor.execute('DELETE FROM carrinhos WHERE user_id = ? AND produto_id = ?', (user_id,produto_id))
            self.commit()
        except sqlite3.OperationalError:
            print('Erro ao remover produto do carrinho')
            
#------------------------------------{Area de cookie}------------------------------------#
            
    def add_session(self,user_id, user_type, session_id, expires_at):
        try:
            self.cursor.execute('INSERT INTO sessions (user_id, user_type, session_id, expires_at) VALUES (?,?,?,?)', (user_id, user_type, session_id, expires_at))
            self.commit()
        except sqlite3.OperationalError as e:
            print('Erro ao criar sessão:', e)


    def create_session(self,user_id, user_type):
        try:
            session_id = str(uuid.uuid4())
            expires_at = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

            self.add_session(user_id, user_type, session_id, expires_at)
            response.set_cookie('session_id', session_id, max_age=3600)

            return session_id
        except sqlite3.OperationalError as e:
            print('Erro ao criar sessão:', e)
            return None


    def delete_session(self,session_id):
        try:
            self.cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
            response.delete_cookie('session_id')
            self.commit()
        except sqlite3.OperationalError as e:
            print('Erro ao deletar sessão:', e)
            
