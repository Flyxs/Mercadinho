function atualizarQuantidade(delta, produtoId) {
    let quantidadeElem = document.getElementById(`quantidade_${produtoId}`);
    let quantidadeInput = document.getElementById(`input_quantidade_${produtoId}`);
    let quantidadeDisponivel = parseInt(document.getElementById(`quantidade_disponivel_${produtoId}`).innerText, 10);
    
    let novaQuantidade = parseInt(quantidadeElem.innerText, 10) + delta;

    if (novaQuantidade < 0) {
        novaQuantidade = 0; // Evita valores menores que 0
    } else if (novaQuantidade > quantidadeDisponivel) {
        novaQuantidade = quantidadeDisponivel; // Evita ultrapassar o estoque máximo
    }

    quantidadeElem.innerText = novaQuantidade;
    quantidadeInput.value = novaQuantidade; // Atualiza o input escondido
}
