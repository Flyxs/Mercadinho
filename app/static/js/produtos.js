function atualizarQuantidadeComLimite(delta, produtoId, limite) {
    let quantidadeElem = document.getElementById(`quantidade_${produtoId}`);
    let quantidadeInput = document.getElementById(`input_quantidade_${produtoId}`);
    
    let novaQuantidade = parseInt(quantidadeElem.innerText, 10) + delta;

    if (novaQuantidade < 0) {
        novaQuantidade = 0; // Evita valores menores que 0
    } else if (limite !== undefined && novaQuantidade > limite) {
        novaQuantidade = limite; // Evita ultrapassar o limite (ex. estoque máximo)
    }

    // Atualizar o texto na interface
    quantidadeElem.innerText = novaQuantidade;
    
    // Atualizar o valor do input escondido
    quantidadeInput.value = novaQuantidade;
}


function atualizarQuantidade(delta, produtoId) {
    let quantidadeDisponivel = parseInt(document.getElementById(`quantidade_disponivel_${produtoId}`).innerText, 10);
    atualizarQuantidadeComLimite(delta, produtoId, quantidadeDisponivel);
}

function atualizarQuantidade_f(delta, produtoId) {
    atualizarQuantidadeComLimite(delta, produtoId, 100);
}

