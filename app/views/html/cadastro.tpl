<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Cadastro</title>
</head>
<body>
    <h1>Cadastro de Usuário</h1>

    <form method="POST">
        %if error_message:
            <p style="color: red; font-weight: bold;">{{ error_message }}</p>
        %end
        <label for="nome">Nome:</label>
        <input type="text" id="nome" name="nome" ><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" ><br><br>

        <label for="cpf">CPF:</label>
        <input type="text" id="cpf" name="cpf" ><br><br>

        <label for="senha">Senha:</label>
        <input type="password" id="senha" name="senha" ><br><br>

        <button type="submit">Cadastrar</button>        
    </form>
    %end
</body>
</html>
