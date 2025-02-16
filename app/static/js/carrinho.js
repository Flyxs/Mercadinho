document.addEventListener("DOMContentLoaded", function () {
    const formCompra = document.getElementById("compraForm");
    
    if (formCompra) {
        formCompra.addEventListener("submit", function (event) {
            event.preventDefault(); // Impede o envio imediato

            mostrarModal(); // Exibe o modal

            // Aguarda 5 segundos e então envia o formulário normalmente
            setTimeout(() => {
                formCompra.submit();
            }, 5000);
        });
    }
});

function mostrarModal() {
    const modal = document.getElementById("myModal");
    if (modal) {
        modal.style.display = "block";
    }
}
