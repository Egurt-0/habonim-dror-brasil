# Guia para editar o site à mão

Guia rápido de onde fica cada coisa no site do Habonim Dror Brasil. As regras do projeto
(LGPD, cores, decisões) ficam no `CLAUDE.md`. As instruções de fotos ficam em
`static/img/LEIA-ME.txt`.

## Antes de tudo: muito texto NÃO está no HTML

Boa parte dos textos vem do **banco de dados** e é editada no **painel (admin)**, no
endereço que está em `DJANGO_ADMIN_URL` no arquivo `.env`.

| No painel | O que se edita |
|---|---|
| Core → Blocos de texto | Textos das páginas (títulos, parágrafos, slogan, política de privacidade) |
| Core → Tópicos | Os cards da home (título, frase, link, ordem) |
| Movimento | Pilares, números, linha do tempo, tochniot |
| Glossário → Termos | Termos em hebraico e suas definições |
| Snifim | História, resumo, Instagram, ordem, foto de capa, galeria, Bagrut |

**Regra prática:** no HTML, frase escrita entre as tags se muda no HTML; se aparece
`{{ alguma_coisa }}`, o texto vem do banco e se muda no painel.

Para a idade do movimento, nunca escreva "81". No painel, escreva `{anos}`, que vira o número
certo a cada ano.

## Como uma página é montada

Exemplo com `/bases/`:

```
1. config/urls.py              → manda "bases/" para o app movimento
2. apps/movimento/urls.py      → "bases/" chama a função views.bases
3. apps/movimento/views.py     → busca os textos no banco e chama o template
4. apps/movimento/templates/movimento/bases.html  → monta o meio da página
5. templates/base.html         → moldura em volta: topo, menu e rodapé
```

Para mudar só o visual, mexa nos passos 4 e 5 e no CSS.

## As pastas

```
habonim-dror-brasil/
├── templates/
│   ├── base.html              ← topo (logo, menu), rodapé e <head>. Vale para TODAS as páginas
│   ├── 404.html / 500.html    ← páginas de erro
│   └── includes/              ← pedaços reaproveitados (topo das páginas, números, seções)
├── apps/
│   ├── core/                  ← home, privacidade, menu, sitemap, robots
│   ├── movimento/             ← Bases, Shichavot Tzeirot, Shichavot Bogrot, Kehilá HD
│   ├── snifim/                ← lista de snifim, página de cada snif, Quero saber mais
│   ├── glossario/             ← glossário e o tooltip automático dos termos
│   └── contas/                ← login, cadastro, meus dados, 2FA
├── static/
│   ├── css/site.css           ← TODO o visual: cores, tamanhos, espaços
│   ├── js/site.js             ← menu do celular, submenu, tooltip, troca de fotos
│   └── img/                   ← fotos e logos (ver LEIA-ME.txt)
├── config/                    ← configurações do Django (settings, urls)
├── CLAUDE.md                  ← regras e decisões do projeto
└── GUIA.md                    ← este arquivo
```

Dentro de cada app: `models.py` são as tabelas do banco, `views.py` é a lógica de cada página,
`templates/<app>/` guarda o HTML e `tests/` guarda os testes.

## Qual arquivo é qual página

| Página | Arquivo |
|---|---|
| `/` (home) | `apps/core/templates/core/home.html` |
| `/bases/` | `apps/movimento/templates/movimento/bases.html` |
| `/shichavot-tzeirot/` | `apps/movimento/templates/movimento/shichavot_tzeirot.html` |
| `/shichavot-bogrot/` | `apps/movimento/templates/movimento/shichavot_bogrot.html` |
| `/kehila-hd/` | `apps/movimento/templates/movimento/kehila_hd.html` |
| `/snifim/` (lista) | `apps/snifim/templates/snifim/lista.html` |
| `/snifim/curitiba/` (cada snif) | `apps/snifim/templates/snifim/detalhe.html` (um arquivo para todos) |
| `/quero-saber-mais/` | `apps/snifim/templates/snifim/quero_saber_mais.html` |
| `/glossario/` | `apps/glossario/templates/glossario/lista.html` |
| `/privacidade/` | `apps/core/templates/core/privacidade.html` |
| Login e conta | `apps/contas/templates/contas/` |
| Erro 404 / 500 | `templates/404.html` / `templates/500.html` |

No VS Code, **Ctrl+P** e o nome do arquivo (ex.: `home.html`) abre direto.

## Onde mudar cada coisa

| Quero mudar… | Onde |
|---|---|
| Um texto do site | No painel (ver a primeira seção) |
| Uma frase fixa, como o rótulo de um botão | No `.html` da página |
| Itens do menu (e submenus) | `apps/core/context_processors.py`, função `menu()` |
| Logo, menu ou rodapé | `templates/base.html` |
| Cores | `static/css/site.css`, no topo (`:root`) |
| Tamanho, espaço ou fonte de algo | `static/css/site.css` (ver "Como achar o CSS") |
| Fotos | `static/img/`, com o nome certo (ver `static/img/LEIA-ME.txt`) |
| Ordem dos snifim | Painel → Snifim → campo "ordem" (menor aparece primeiro) |
| Páginas no Google (sitemap) | `PAGINAS_DO_SITEMAP` em `apps/core/views.py` |

## Como achar o CSS de um elemento

1. No navegador, clique com o botão direito no elemento e escolha **Inspecionar**.
2. Veja a `class="..."` dele, por exemplo `class="topico__titulo"`.
3. No VS Code, **Ctrl+Shift+F** e busque `.topico__titulo`.

Os nomes seguem o padrão `bloco__parte--variacao`: `topico` é o card, `topico__titulo` é o
título do card e `topico--sem-foto` é o card sem foto.

## Os símbolos do HTML (templates do Django)

| Símbolo | O que faz |
|---|---|
| `{{ snif.nome }}` | Mostra um dado (do banco ou da view) |
| `{% if ... %} ... {% endif %}` | Só mostra se a condição for verdadeira |
| `{% for snif in snifim %} ... {% endfor %}` | Repete para cada item |
| `{% url 'snifim:lista' %}` | Gera o link de uma página (não escreva `/snifim/` à mão) |
| `{% static 'css/site.css' %}` | Link para um arquivo de `static/` |
| `{% block conteudo %}` | "Buraco" do `base.html` que cada página preenche |
| `{% include "includes/..." %}` | Encaixa um pedaço reaproveitado |
| `\|com_glossario` | Liga os termos em hebraico ao glossário (com tooltip) |
| `{# ... #}` ou `{% comment %}` | Comentário (não aparece no site) |

## Regras de ouro

- **Cores:** só vermelho e branco, sempre com as variáveis (`var(--vermelho)`,
  `var(--vermelho-escuro)`, `var(--branco)`), nunca com código de cor solto.
- **Logos:** só os arquivos oficiais de `static/img/logos/`. Nunca redesenhar nem recolorir.
- **Fotos com pessoas:** só com autorização ou com ninguém identificável (de costas ou de longe).
  Galeria e Bagrut só aparecem com "publicação autorizada" marcada.
- **Contato publicado:** sempre institucional do snif, nunca o número pessoal de um menor.
- **Idade do movimento:** `{anos}` no painel, `{{ anos_de_movimento }}` no HTML.
- **Nada de terceiros:** sem Google Fonts, Analytics, pixels ou embeds de Instagram. Link
  simples pode.

## Foto com algo que não deve aparecer (ponto a esconder)

Se uma foto tem um detalhe que precisa ficar coberto pelo título (por exemplo, um rosto
deformado), dá para marcar esse ponto no CSS. O site posiciona a foto sozinho, em qualquer
tela, para o ponto ficar embaixo das letras. Em `static/css/site.css`, bloco
`/* Ponto a esconder */`:

```css
.hero__foto[style*="nome-do-arquivo"] { --esconder-x: 0.337; --esconder-y: 0.515; }
```

- `--esconder-x` é a posição horizontal do ponto, de 0 (esquerda) a 1 (direita).
- `--esconder-y` é a posição vertical, de 0 (topo) a 1 (base).
- Para calcular, divida a posição do ponto em pixels pelo tamanho da foto. Ex.: rosto em
  691 × 685 numa foto de 2048 × 1329 dá 691 / 2048 = 0,337 e 685 / 1329 = 0,515.
- Funciona em `.hero__foto` (fundo da home), `.topico` (cards) e `.cabecalho-pagina` (topo das
  páginas). Trocou a foto? Apague a linha dela.

## Depois de editar

1. Salve. O `runserver` recarrega sozinho. No navegador, **Ctrl+F5** (recarrega sem cache).
2. Mexeu em código Python? Rode os testes: `pytest`.
3. Lint e formatação: `ruff check .` e `ruff format .`.
4. Salvar no GitHub:
   ```
   git add .
   git commit -m "o que mudou"
   git push
   ```

## Comandos úteis

```
.venv\Scripts\activate              # ativa o ambiente Python (Windows)
python manage.py runserver          # sobe o site em http://127.0.0.1:8000
python manage.py migrate            # aplica mudanças no banco
python manage.py createsuperuser    # cria uma conta de administrador
pytest                              # roda os testes
```
