<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Cadastro</title>
    <link rel="stylesheet" type="text/css" href="static/css/cadastro.css">
</head>
<body>

    <div class="voltar">
        <form action="/" method="get">
            <button type="submit" aria-label="Voltar para a página inicial">Voltar</button>
        </form>
    </div>

    <div class="container">
        <h1>Cadastro de Usuário</h1>

        %if error_message:
            <p class="error-message">{{ error_message }}</p>
        %end

        <form method="POST">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <label for="cpf">CPF:</label>
            <input type="text" id="cpf" name="cpf" required>

            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" required>

            <button type="submit" class="btn">Cadastrar</button>        
        </form>
    </div>
</body>
</html>

