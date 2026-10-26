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

  // Submenus (ex.: Shichavot): o botão abre e fecha (clique, toque, Enter); Esc, clique fora
  // ou Tab para fora fecham. Passar o mouse por cima abre só com CSS.
  const grupos = document.querySelectorAll(".menu__grupo");
  const fecharGrupo = (grupo) => {
    grupo.classList.remove("aberto");
    grupo.querySelector(".menu__grupo-botao").setAttribute("aria-expanded", "false");
  };
  grupos.forEach((grupo) => {
    const botaoGrupo = grupo.querySelector(".menu__grupo-botao");
    botaoGrupo.addEventListener("click", () => {
      const aberto = grupo.classList.toggle("aberto");
      botaoGrupo.setAttribute("aria-expanded", String(aberto));
    });
    grupo.addEventListener("focusout", (evento) => {
      if (!grupo.contains(evento.relatedTarget)) fecharGrupo(grupo);
    });
  });
  document.addEventListener("click", (evento) => {
    grupos.forEach((grupo) => {
      if (!grupo.contains(evento.target)) fecharGrupo(grupo);
    });
  });
  document.addEventListener("keydown", (evento) => {
    if (evento.key !== "Escape") return;
    grupos.forEach((grupo) => {
      if (grupo.classList.contains("aberto")) {
        fecharGrupo(grupo);
        grupo.querySelector(".menu__grupo-botao").focus();
      }
    });
  });

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

  // Fotos com um ponto a esconder (CSS --esconder-x/--esconder-y, frações da foto): posiciona
  // a foto para esse ponto ficar sob as letras do título, na tela de quem está vendo.
  const tamanhos = new Map();
  const tamanhoDaFoto = (url) => {
    if (!tamanhos.has(url)) {
      tamanhos.set(url, new Promise((ok) => {
        const img = new Image();
        img.onload = () => ok([img.naturalWidth, img.naturalHeight]);
        img.onerror = () => ok(null);
        img.src = url;
      }));
    }
    return tamanhos.get(url);
  };
  const ZOOMS = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6];
  const esconderPonto = async (el) => {
    el.style.backgroundSize = "";
    el.style.backgroundPosition = "";
    const css = getComputedStyle(el);
    const fx = parseFloat(css.getPropertyValue("--esconder-x"));
    const fy = parseFloat(css.getPropertyValue("--esconder-y"));
    // O navegador devolve url("..."); o nome do arquivo pode ter parênteses, ex.: "foto (1).png"
    const url = (css.backgroundImage.match(/^url\("(.*)"\)$/) || [])[1];
    if (Number.isNaN(fx) || Number.isNaN(fy) || !url) return;
    const tamanho = await tamanhoDaFoto(url);
    if (!tamanho) return;
    const [iw, ih] = tamanho;
    const caixa = el.closest(".hero") || el;  // a foto do hero tem transform; mede o hero
    const texto = el.classList.contains("hero__foto")
      ? caixa.querySelector(".hero__titulo")
      : el.querySelector(".topico__titulo, h1");
    if (!texto) return;
    const r = caixa.getBoundingClientRect();
    const intervalo = document.createRange();
    intervalo.selectNodeContents(texto);
    const linhas = [...intervalo.getClientRects()];
    for (const zoom of ZOOMS) {
      const escala = Math.max(r.width / iw, r.height / ih) * zoom;
      const w = iw * escala, h = ih * escala, px = fx * w, py = fy * h;
      const yNatural = (r.height - h) / 2 + py;
      // Meio das letras maiúsculas de cada linha, da linha mais perto do ponto para a mais longe
      const alvos = linhas
        .map((l) => ({ l, y: l.top - r.top + l.height * 0.56 }))
        .sort((a, b) => Math.abs(a.y - yNatural) - Math.abs(b.y - yNatural));
      for (const { l, y } of alvos) {
        const deslocY = y - py;
        if (deslocY > 0 || deslocY < r.height - h) continue;
        const xMin = Math.max(l.left - r.left + l.width * 0.1, r.width - w + px);
        const xMax = Math.min(l.right - r.left - l.width * 0.1, px);
        if (xMin > xMax) continue;
        const x = Math.min(xMax, Math.max(xMin, (r.width - w) / 2 + px));
        el.style.backgroundSize = `${w}px ${h}px`;
        el.style.backgroundPosition = `${x - px}px ${deslocY}px`;
        return;
      }
    }
    // Sem posição possível: fica o enquadramento do CSS.
  };
  const esconderPontos = () => {
    document.querySelectorAll(".hero__foto, .topico, .cabecalho-pagina").forEach(esconderPonto);
  };
  esconderPontos();
  if (document.fonts) document.fonts.ready.then(esconderPontos);
  let espera;
  window.addEventListener("resize", () => {
    clearTimeout(espera);
    espera = setTimeout(esconderPontos, 150);
  });

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
