<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h2>Login</h2>
    
    <form action="/login" method="post">

        % if error_message:
            <p style="color:red;">{{error_message}}</p>
        % end

        <label>Email:</label>
        <input type="email" id="email" name="email" required>
        <br>
        <label>Senha:</label>
        <input type="password" name="senha" required>
        <br>
        <input type="submit" value="Entrar">
    </form>
</body>
</html>