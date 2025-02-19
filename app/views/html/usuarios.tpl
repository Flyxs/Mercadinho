<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="static/css/usuarios.css">
    <script src="static/js/usuarios.js" defer></script>
    <title>Usuarios</title>
</head>
<body>

    <!-- 📌 Botão para voltar ao Dashboard -->
    <div class="voltar">
        <form action="/dashboard_f" method="get">
            <button type="submit" aria-label="Voltar para o dashboard">Voltar</button>
        </form>
    </div>

    <!-- 📌 Botões para exibir clientes ou funcionários -->
    <div class="show_clientes">
        <form action="/usuarios" method="POST">
            <input type="hidden" name="show_cliente" value="1">
            <button type="submit" aria-label="Ir para clientes">Clientes</button>
        </form>
    </div>

    <div class="show_funcionarios">
        <form action="/usuarios" method="POST">
            <input type="hidden" name="show_funcionario" value="1">
            <button type="submit" aria-label="Ir para funcionarios">Funcionários</button>
        </form>
    </div>

    <!-- 📌 Lista de clientes -->
    % if show_cliente:
        <div class="clientes">
            % for cliente in clientes:
                <div class="cliente">
                    <h2>{{ cliente[2] }}</h2>
                    <p>Email: {{ cliente[3] }}</p>
                    <p>CPF: {{ cliente[4] }}</p>

                    <div class="botoes_cliente">
                        <form method="post">
                            <input type="hidden" name="promover" value="{{ cliente[3] }}">
                            <button type="submit">Promover a funcionário</button>
                        </form>
                        <form method="post">
                            <input type="hidden" name="excluir" value="{{ cliente[3] }}">
                            <button type="submit">Excluir</button>
                        </form>
                    </div>
                </div>
            % end
        </div>  
    % end

    <!-- 📌 Lista de funcionários -->
    % if show_funcionario:
        <div class="funcionarios">
            % for funcionario in funcionarios:
                <div class="funcionario">
                    <h2>{{ funcionario[2] }}</h2>
                    <p>Email: {{ funcionario[3] }}</p>
                    <p>CPF: {{ funcionario[4] }}</p>
                    <p>Salário: R$ {{ funcionario[6] }}</p>

                    <div class="botoes_funcionario">
                        <form method="post">
                            <input type="hidden" name="rebaixar" value="{{ funcionario[3] }}">
                            <button type="submit">Rebaixar a cliente</button>
                        </form>
                        <form method="post">
                            <input type="hidden" name="promover" value="{{ funcionario[3] }}">
                            <button type="submit">Promover a gerente</button>
                        </form>
                        <form method="post">
                            <input type="hidden" name="excluir" value="{{ funcionario[3] }}">
                            <button type="submit">Excluir</button>
                        </form>
                    </div>
                </div>
            % end
        </div>  
    % end

</body>
</html>

