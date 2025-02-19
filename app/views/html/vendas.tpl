<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vendas</title>
    <link rel="stylesheet" type="text/css" href="static/css/vendas.css">
    <script src="static/js/vendas.js" defer></script>
</head>
<body>
    
    <div class="voltar">
        <form action="/dashboard_f" method="get">
            <button type="submit" arial-label="Voltar para o dashboard">Voltar</button>
        </form>
    </div>

    <div class="saldo">
        <h2>Saldo da conta</h2>
        <div class="tabela">
            <table>
                <tr>
                    <th>Receita</th>
                    <th>Despesa</th>
                    <th>Total</th>
                </tr>
                <tr>
                    <td>R${{ saldo[0] }}</td>
                    <td>R${{ saldo[1] }}</td>
                    <td>R${{ saldo[2] }}</td>
                </tr>
            </table>
        </div>
    </div>


    <div class="vendas">
        <h2>Transações</h2>
        <div class="tabela">
            <p>Ultimas 20 transações</p>
            <table>
                <tr>
                    <th>Data</th>
                    <th>Horário</th>
                    <th>Valor</th>
                    <th>Tipo</th>
                </tr>
                % for transacao in transacoes[::-1][:20]:
                    <tr>
                        <td>{{ transacao[1] }}</td>
                        <td>{{ transacao[2] }}</td>
                        <td>R${{ transacao[3] }}</td>
                        <td>{{ transacao[4] }}</td>
                    </tr>
                % end
            </table>
        </div>
    </div>
</body>
</html>