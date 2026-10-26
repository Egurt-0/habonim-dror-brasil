// Comportamentos pequenos do site. Sem dependências.
// Sem JavaScript o site continua funcionando: o menu fica aberto (ver <noscript> no base.html).

document.addEventListener("DOMContentLoaded", () => {
  // Menu no celular: abre/fecha no botão, fecha com Esc e ao escolher um link.
  const botao = document.querySelector(".topo__menu-botao");
  const menu = document.getElementById("menu-principal");
  if (botao && menu) {
    const fechar = () => {
      menu.classList.remove("aberto");
      botao.setAttribute("aria-expanded", "false");
    };
    botao.addEventListener("click", () => {
      const aberto = menu.classList.toggle("aberto");
      botao.setAttribute("aria-expanded", String(aberto));
    });
    menu.addEventListener("click", (evento) => {
      if (evento.target.closest("a")) fechar();
    });
    document.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape" && menu.classList.contains("aberto")) {
        fechar();
        botao.focus();
      }
    });
  }

  // Fotos do fundo da home: troca suave a cada 7 segundos (se houver mais de uma).
  const fotos = document.querySelectorAll(".hero__foto");
  const semMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (fotos.length > 1 && !semMovimento) {
    let atual = 0;
    setInterval(() => {
      fotos[atual].classList.remove("ativa");
      atual = (atual + 1) % fotos.length;
      fotos[atual].classList.add("ativa");
    }, 7000);
  }

  // Termos do glossário: a caixa da definição é empurrada para dentro da tela perto das bordas.
  const MARGEM = 12;
  const posicionar = (termo) => {
    const caixa = termo.querySelector(".termo__definicao");
    if (!caixa) return;
    caixa.style.setProperty("--desloca", "0px");
    const { left, right } = caixa.getBoundingClientRect();
    const largura = document.documentElement.clientWidth;
    let desloca = 0;
    if (left < MARGEM) desloca = MARGEM - left;
    else if (right > largura - MARGEM) desloca = largura - MARGEM - right;
    caixa.style.setProperty("--desloca", `${desloca}px`);
  };
  document.querySelectorAll(".termo").forEach((termo) => {
    termo.addEventListener("mouseenter", () => posicionar(termo));
    termo.addEventListener("focus", () => posicionar(termo));
  });

  // Em telas de toque, o 1º toque mostra a definição e o 2º abre o glossário.
  const semHover = window.matchMedia("(hover: none)").matches;
  if (semHover) {
    document.addEventListener("click", (evento) => {
      const termo = evento.target.closest(".termo");
      document.querySelectorAll(".termo.ativo").forEach((t) => {
        if (t !== termo) t.classList.remove("ativo");
      });
      if (termo && !termo.classList.contains("ativo")) {
        evento.preventDefault();
        posicionar(termo);
        termo.classList.add("ativo");
      }
    });
  }

  // Esc esconde a definição aberta por toque.
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape") {
      document.querySelectorAll(".termo.ativo").forEach((t) => t.classList.remove("ativo"));
    }
  });
});
