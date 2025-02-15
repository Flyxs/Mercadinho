<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/produtos.css">
    <script src="/static/js/produtos.js"></script>
    <title>Produtos</title>
</head>
<body>
    <h1>Produtos</h1>

    <div class="produtos_all">
        % for produto in produtos:

            <div class="produto">
                % if produto[4] > 0:
                    <h2>{{ produto[1] }}</h2>
                    <p>Preço: {{ produto[2] }}</p>
                    <p>Quantidade disponível: <span id="quantidade_disponivel_{{ produto[0] }}">{{ produto[4] }}</span></p>

                    <div>
                        <button type="button" class="decrementar" data-id="{{ produto[0] }}" onclick="diminui( produto[0] )">-</button>
                        <span id="quantidade_{{ produto[0] }}">0</span>
                        <button type="button" class="incrementar" data-id="{{ produto[0] }}" onclick="aumenta( produto[0] )">+</button>
                    </div>

                    <div class="submit info">
                        <form method="post" onsubmit="atualizarQuantidade( produto[0] )">
                            <input type="hidden" name="produto_id" value="{{ produto[0] }}">
                            <input type="hidden" name="quantidade" id="quantidade_input_{{ produto[0] }}" value="0">
                            <button type="submit">Adicionar ao Carrinho</button>   
                        </form>                       
                    </div>

                % end
            </div>

        % end
    </div>

    <form action="/dashboard_c" method="GET">
        <button type="submit" aria-label="Voltar para o dashboard">Voltar</button>
    </form>
    <form action="/carrinho" method="GET">
        <button type="submit" aria-label="Ir para o carrinho">Carrinho</button>
    </form>

</body>
</html>