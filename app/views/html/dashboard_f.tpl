<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="static/css/dashboard_f.css">
    <script src="../../static/js/dashboard_f.js"></script>
    <title>{{user[1]}}</title>
</head>

<body>
    <div class="logout">
        <form action="/logout" method="POST">
            <button type="submit" aria-label="Sair da sessão">Sair</button>
        </form>
    </div>
    
    
    <div class="nome">
        <h1>{{user[2]}}</h1>
        <h3>{{user[3]}}</h3>
    </div>

    <div class="acoes">
        % if user[1] == 'adm':
            <div class="adm">
                <form action="/usuarios" method="GET">
                    <button type="submit" aria-label="Gerenciar usuarios">Gerenciar usuários</button>
                </form>
                <form action="/vendas" method="GET">
                    <button type="submit" aria-label="Consultar vendas">Consultar vendas</button>
                </form>
            </div>
        % end
        <div class="funcionario">
            <form action="/produtos" method="GET">
                <button type="submit" aria-label="Gerenciar produtos">Gerenciar Produtos</button>
            </form>
        </div>
    </div>
</body>
</html>