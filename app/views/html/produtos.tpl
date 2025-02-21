<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/produtos.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>

    <title>Produtos</title>
</head>
<body>
    

    %if user[1] == 'cliente':
    <div class="voltar">
        <form action="/dashboard_c" method="GET">
            <button type="submit" aria-label="Voltar para o dashboard">Voltar</button>
        </form>
    </div>
    %elif user[1] == 'funcionario' or user[1] == 'adm':
    <div class="voltar">
        <form action="/dashboard_f" method="GET">
            <button type="submit" aria-label="Voltar para o dashboard">Voltar</button>
        </form>
    </div>
    %end

    

    <div class="produtos_all">

        <h1>Produtos Disponiveis</h1>

        % if user[1] == 'cliente':



            % if produtos:
                % for produto in produtos:

                    <div class="produto">
                        % if produto[4] > 0:
                            <h2>{{ produto[1] }}</h2>
                            <p>Preço: R${{ produto[2] }}</p>
                            <p>Quantidade disponível: <span id="quantidade_disponivel_{{ produto[0] }}">{{ produto[4] }}</span></p>

                            <div class="quantidade">
                                <button onclick="atualizarQuantidade(-10, {{produto[0]}})">-10</button>
                                <button onclick="atualizarQuantidade(-1, {{produto[0]}})">-</button>
                                <span id="quantidade_{{ produto[0] }}">0</span>
                                <button onclick="atualizarQuantidade(1, {{produto[0]}})">+</button> 
                                <button onclick="atualizarQuantidade(10, {{produto[0]}})">+10</button>
                            </div>

                            <div class="submit info">
                                <form method="post" action="/produtos">
                                    <input type="hidden" name="produto_id" value="{{ produto[0] }}">
                                    <input type="hidden" id="input_quantidade_{{ produto[0] }}" name="quantidade" value="0">
                                    <button type="submit" id="atualizarEstoque">Adicionar ao Carrinho</button>
                                </form>
                                
                            </div>

                        % end
                    </div>

                % end
            % else:
                <p>Estamos sem produtos no momento :(</p>
            % end

        % elif user[1] == 'funcionario' or user[1] == 'adm':

            % if user[1] == 'adm':

                <h3>Adicionar Novo Produto ao Estoque</h3>

                <div class="adicionar_produto">
                    <form method="post">
                        <input type="text" name="nome_produto" id="nome_produto" placeholder="Nome do produto" required>
                        <input type="number" name="preco_venda" placeholder="Preço de venda" min="0" step="0.01" required>
                        <input type="number" name="preco_compra" placeholder="Preço de compra" min="0" step="0.01" required>
                        <select name="tipo" id="tipoProduto" required>
                            <option value="" disabled selected>Selecione um tipo</option>
                            <option value="0">Alimento</option>
                            <option value="1">Limpesa</option>
                            <option value="2">Saude</option>
                            <option value="3">Ferramentas</option>
                            <option value="4">Eletronicos</option>
                            <option value="5">Outros</option>
                        </select>
                        <button type="submit">Adicionar</button>
                    </form>
                </div>


            % end

            % for produto in produtos:


                <div class="produto">

                    <h2>{{ produto[1] }}</h2>
                    <p>Preço: R${{ produto[3] }}</p>
                    <p>Quantidade disponível: <span id="quantidade_disponivel_{{ produto[0] }}">{{ produto[4] }}</span></p>

                    <div class="quantidade">
                        <button onclick="atualizarQuantidade_f(-10, {{produto[0]}})">-10</button>
                        <button onclick="atualizarQuantidade_f(-1, {{produto[0]}})">-</button>
                        <span id="quantidade_{{ produto[0] }}">0</span>
                        <button onclick="atualizarQuantidade_f(1, {{produto[0]}})">+</button> 
                        <button onclick="atualizarQuantidade_f(10, {{produto[0]}})">+10</button>
                    </div>

                    <div class="submit info">
                        <form method="post" action="/produtos">
                            <input type="hidden" name="produto_id" value="{{ produto[0] }}">
                            <input type="hidden" id="input_quantidade_{{ produto[0] }}" name="quantidade" value="0">
                            <button type="submit" id="atualizarEstoque">Comprar Produtos</button> 
                        </form>
                        % if user[1] == 'adm':
                            <form method="post" action="/produtos">
                                <input type="hidden" name="excluir_produto" value="{{ produto[0] }}">
                                <button type="submit">Excluir Produto</button>
                            </form>
                        % end
                        </form>
                        
                    </div>

                </div>

            % end
        % end
    </div>


    <script src="/static/js/produtos.js"></script>
</body>
</html>