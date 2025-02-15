document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todos os botões de incrementar
    document.querySelectorAll(".incrementar").forEach(button => {
        button.addEventListener("click", function () {
            let id = this.getAttribute("data-id");
            let quantidadeSpan = document.getElementById("quantidade_" + id);
            let inputQuantidade = document.getElementById("input_quantidade_" + id);
            let quantidadeMaxima = parseInt(document.getElementById("quantidade_disponivel_" + id).textContent); // Pega o estoque disponível

            let quantidade = parseInt(quantidadeSpan.textContent);
            if (quantidade < quantidadeMaxima) {
                quantidade++; // Incrementa apenas se não atingir o limite
                quantidadeSpan.textContent = quantidade;
                inputQuantidade.value = quantidade;
            }
        });
    });

    // Seleciona todos os botões de decrementar
    document.querySelectorAll(".decrementar").forEach(button => {
        button.addEventListener("click", function () {
            let id = this.getAttribute("data-id");
            let quantidadeSpan = document.getElementById("quantidade_" + id);
            let inputQuantidade = document.getElementById("input_quantidade_" + id);

            let quantidade = parseInt(quantidadeSpan.textContent);
            if (quantidade > 0) {
                quantidade--; // Decrementa apenas se for maior que 0
                quantidadeSpan.textContent = quantidade;
                inputQuantidade.value = quantidade;
            }
        });
    });
});


// Função para diminuir a quantidade
function diminui(produtoId) {
    var quantidadeSpan = document.getElementById("quantidade_" + produtoId);
    var quantidadeAtual = parseInt(quantidadeSpan.textContent);
    if (quantidadeAtual > 0) {
        quantidadeSpan.textContent = quantidadeAtual - 1;
    }
}

// Função para aumentar a quantidade
function aumenta(produtoId) {
    var quantidadeSpan = document.getElementById("quantidade_" + produtoId);
    var quantidadeAtual = parseInt(quantidadeSpan.textContent);
    var quantidadeDisponivel = parseInt(document.getElementById("quantidade_disponivel_" + produtoId).textContent);
    
    if (quantidadeAtual < quantidadeDisponivel) {
        quantidadeSpan.textContent = quantidadeAtual + 1;
    }
}

// Função para atualizar o valor no input hidden antes de enviar o formulário
function atualizarQuantidade(produtoId) {
    var quantidadeSpan = document.getElementById("quantidade_" + produtoId);
    var quantidadeInput = document.getElementById("quantidade_input_" + produtoId);
    quantidadeInput.value = quantidadeSpan.textContent;
}
