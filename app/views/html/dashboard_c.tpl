<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="static/css/index.css">
    <script src="../../static/js/index.js"></script>
    <title>Home</title>
</head>

<body>
    <h1>{{user[2]}}</h1>
    <br>
    <form action="/logout" method="POST">
        <button type="submit" aria-label="Sair da sessão">Sair</button>
    </form>
    <form action="/produtos" method="GET">
        <button type="submit" aria-label="Ir para produtos">Produtos</button>
    </form>
</body>
</html>