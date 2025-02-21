import socketio
from app.controllers.application import Application

sio = socketio.Server(cors_allowed_origins="*")
ctl = Application()

@sio.event
def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

@sio.on('atualizar_estoque')
def atualizar_estoque(data):
    produto_id = data.get('produto_id')
    nova_quantidade = data.get('quantidade')

    print(f"🔄 Recebendo atualização de estoque | Produto: {produto_id} | Nova Quantidade: {nova_quantidade}")

    # Enviar atualização para todos os clientes conectados
    sio.emit('estoque_atualizado', {
        'produto_id': produto_id,
        'quantidade': nova_quantidade
    })
    print(f"📡 Enviando atualização para os clientes...")


@sio.event
def disconnect(sid, environ):
    print(f"Cliente desconectado: {sid}")

# Criando a aplicação WebSocket
ws_app = socketio.WSGIApp(sio)

