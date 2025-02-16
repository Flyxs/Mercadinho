<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/carrinho.css">
    <script src="/static/js/carrinho.js" defer></script>
    <title>Carrinho</title>
</head>

<body>
    <h1>Carrinho</h1>

    <form action="/produtos" method="GET">
        <button type="submit" aria-label="Voltar para produtos">Produtos</button>
    </form>    

    <div class="carrinho">
        % if not carrinho:
            <p>{{ mensagem }}</p>
        % else:
            <h2>Produtos no carrinho:</h2>
            % for produto in carrinho:
                <div class="produtos">
                    <div class="info_produto">
                        <h3>{{ produto[1] }}</h3>
                        <p>Quantidade: {{ produto[2] }}</p>
                        <p>Preço: R${{ produto[3] * produto[2] }}</p>
                    </div>

                    <div class="cancelar_produto">
                        <form method="post">
                            <input type="hidden" name="quantidade" value="{{ produto[2] }}">
                            <input type="hidden" name="cancelar_produto" value="{{ produto[0] }}">
                            <button type="submit">Cancelar</button>
                        </form>
                    </div>

                </div>
            % end
        % end
    </div>

    <div class="total">
        <h2>Total a pagar: R${{ total }}</h2>
    </div>

    <div class="botoes-container">
        <div class="confirmar_compra">  
            <form id="compraForm" method="post" onsubmit="mostrarModal(event)">
                <button type="submit" class="btn confirmar">Confirmar Compra</button>
            </form>
        </div>
    
        <div class="cancelar_carrinho">
            <form method="post">
                <input type="hidden" name="cancelar_carrinho" value="1">
                <button type="submit" class="btn cancelar">Cancelar Tudo</button>
            </form>
        </div>
    </div>

    <!-- Modal de Confirmação -->
    <div id="myModal" class="modal">
        <div class="modal-content">
            <h2>Compra Confirmada!</h2>
            <p>Seu pedido foi confirmado com sucesso.</p>
            <div class="modal-buttons">
                <button onclick="fecharModal()">Fechar</button>
            </div>
        </div>
    </div>


</body>
</html>