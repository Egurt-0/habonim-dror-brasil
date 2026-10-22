// Comportamentos pequenos do site. Sem dependências.

document.addEventListener("DOMContentLoaded", () => {
  // Menu no celular
  const botao = document.querySelector(".topo__menu-botao");
  const menu = document.getElementById("menu-principal");
  if (botao && menu) {
    botao.addEventListener("click", () => {
      const aberto = menu.classList.toggle("aberto");
      botao.setAttribute("aria-expanded", String(aberto));
    });
  }

  // Termos do glossário: em telas de toque, o 1º toque mostra a definição e o 2º abre o glossário.
  const semHover = window.matchMedia("(hover: none)").matches;
  if (semHover) {
    document.addEventListener("click", (evento) => {
      const termo = evento.target.closest(".termo");
      document.querySelectorAll(".termo.ativo").forEach((t) => {
        if (t !== termo) t.classList.remove("ativo");
      });
      if (termo && !termo.classList.contains("ativo")) {
        evento.preventDefault();
        termo.classList.add("ativo");
      }
    });
  }
});
