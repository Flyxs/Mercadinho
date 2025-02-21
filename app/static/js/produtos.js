// Conectar ao servidor WebSocket
const socket = io('http://localhost:8080');

// Função para atualizar a quantidade com limite
function atualizarQuantidadeComLimite(delta, produtoId, limite) {
    let quantidadeElem = document.getElementById(`quantidade_${produtoId}`);
    let quantidadeInput = document.getElementById(`input_quantidade_${produtoId}`);
    let novaQuantidade = parseInt(quantidadeElem.innerText, 10) + delta;

    if (novaQuantidade < 0) {
        novaQuantidade = 0; // Evita valores menores que 0
    } else if (limite !== undefined && novaQuantidade > limite) {
        novaQuantidade = limite; // Evita ultrapassar o limite máximo
    }

    // Atualizar o texto na interface
    quantidadeElem.innerText = novaQuantidade;
    quantidadeInput.value = novaQuantidade;

    
    }


// Função para atualizar quantidade do cliente, respeitando o estoque
function atualizarQuantidade(delta, produtoId) {
    let quantidadeDisponivel = parseInt(document.getElementById(`quantidade_disponivel_${produtoId}`).innerText, 10);
    atualizarQuantidadeComLimite(delta, produtoId, quantidadeDisponivel);
}

// Função para atualizar quantidade para funcionários (limite maior)
function atualizarQuantidade_f(delta, produtoId) {
    atualizarQuantidadeComLimite(delta, produtoId, 100);
}


// Escutando o evento 'estoque_atualizado' emitido pelo servidor
socket.on('estoque_atualizado', (data) => {
    console.log(`Produto ${data.produto_id} atualizado para quantidade: ${data.quantidade}`);

    // Atualizar a quantidade em todos os elementos da página
    let quantidadeElem = document.getElementById(`quantidade_${data.produto_id}`);
    let quantidadeInput = document.getElementById(`input_quantidade_${data.produto_id}`);
    
    if (quantidadeElem && quantidadeInput) {
        quantidadeElem.innerText = data.quantidade;
        quantidadeInput.value = data.quantidade;
    }
});
