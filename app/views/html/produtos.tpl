<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/produtos.css">
    <script src="/static/js/produtos.js" defer></script>
    <title>Produtos</title>
</head>
<body>
    <h1>Produtos</h1>

    <form action="/dashboard_c" method="GET">
        <button type="submit" aria-label="Voltar para o dashboard">Voltar</button>
    </form>
    <form action="/carrinho" method="GET">
        <button type="submit" aria-label="Ir para o carrinho">Carrinho</button>
    </form>


    <div class="produtos_all">
        % if produtos:
            % for produto in produtos:

                <div class="produto">
                    % if produto[4] > 0:
                        <h2>{{ produto[1] }}</h2>
                        <p>Preço: R${{ produto[2] }}</p>
                        <p>Quantidade disponível: <span id="quantidade_disponivel_{{ produto[0] }}">{{ produto[4] }}</span></p>

                        <div class="quantidade">
                            <button onclick="atualizarQuantidade(-1, {{produto[0]}})">-</button>
                            <span id="quantidade_{{ produto[0] }}">0</span>
                            <button onclick="atualizarQuantidade(1, {{produto[0]}})">+</button> 
                        </div>

                        <div class="submit info">
                            <form method="post" action="/produtos">
                                <input type="hidden" name="produto_id" value="{{ produto[0] }}">
                                <input type="hidden" id="input_quantidade_{{ produto[0] }}" name="quantidade" value="0">
                                <button type="submit">Adicionar ao Carrinho</button>
                            </form>
                            
                        </div>

                    % end
                </div>

            % end
        % else:
            <p>Estamos sem produtos no momento :(</p>
        % end
    </div>



</body>
</html>