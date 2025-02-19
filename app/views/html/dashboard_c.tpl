<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="static/css/dashboard_c.css">
    <script src="../../static/js/dasboard_c.js"></script>
    <title>Home</title>
</head>

<body>

    <div class="botoes">
        <div class="logout">
            <form action="/logout" method="POST">
                <button type="submit" aria-label="Sair da sessão">Sair</button>
            </form>
        </div>
        <div class="produtos"></div>
            <form action="/produtos" method="GET">
                <button type="submit" aria-label="Ir para produtos">Produtos</button>
            </form>
        </div>
    </div>

    
    <div class="Nome">
        <h1>{{user[2]}}</h1>
    </div>

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
        % if carrinho:
            <div class="confirmar_compra">  
                <form id="compraForm" method="post">
                    <input type="hidden" name="confirmar_compra" value="1">
                    <button type="submit" class="btn confirmar">Confirmar Compra</button>
                </form>                
            </div>
        
            <div class="cancelar_carrinho">
                <form method="post">
                    <input type="hidden" name="cancelar_carrinho" value="1">
                    <button type="submit" class="btn cancelar">Cancelar Tudo</button>
                </form>
            </div>
        % end
    </div>


</body>
</html>