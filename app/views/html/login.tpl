<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="/static/css/login.css">
</head>
<body>

    <div class="voltar">
        <form action="/" method="get">
            <button type="submit" aria-label="Voltar para a página inicial">Voltar</button>
        </form>
    </div>

    <div class="container">
        <h1>Login</h1>
        

        <form action="/login" method="post">

            % if error_message:
                <p class="error-message">{{error_message}}</p>
            % end

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" required>

            <div class="buttons">
                <input type="submit" class="btn" value="Entrar">
            </div>
        </form>
    </div>
</body>
</html>
