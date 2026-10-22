# Habonim Dror Brasil — site

Site do **Habonim Dror Brasil (HDBR)**, movimento juvenil judaico (tnuá) sionista socialista,
chalutziano e kibutziano, presente no Brasil desde 1945.

## Objetivo

Um site que **apresenta o movimento** para quem não o conhece (pais, comunidade, possíveis
chanichim, parceiros, doadores), com **login opcional** e uma **área de doações**. O material
de divulgação define três argumentos centrais, que devem guiar texto e layout:

1. **Capilaridade nacional**: não é uma tnuá local, é uma rede que conecta o Brasil inteiro.
2. **Alcance**: chega a crianças sem escola judaica ou outras opções de educação judaica.
3. **Impacto comunitário**: forma as lideranças que sustentam as pequenas comunidades.

Slogan: **"80 anos formando líderes, construindo comunidade e conectando gerações."**

O site vai crescer. **Toda decisão deve facilitar adicionar features depois**, sem reescrever
o que existe.

### Escopo decidido

- **Acesso anônimo e logado**: todo o conteúdo institucional é público. O login é opcional e
  existe para recursos como histórico de doações e aparecer no ranking.
- **Sem loja.** O site não vende nada (nem o Vinho Guefen, que aparece só como informação, com
  o contato do snif).
- **Área de doações** com **ranking de doadores** e **opção de doação anônima sempre disponível**.
- **Uma página por snif**, com dados, história, galeria de imagens e foto da Bagrut.

## Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Linguagem | Python 3.12 | O dono do projeto mexe com Python com mais segurança |
| Framework | **Django 5.2 LTS** | Auth, admin, ORM, migrations, forms e CSRF prontos; suporte até 2028 |
| Banco | **PostgreSQL** (dev e produção) | Decidido. Usar Postgres também em dev para não haver diferença entre ambientes |
| Front | Templates Django + CSS próprio; **HTMX** quando precisar de interatividade | Sem build de JS, sem SPA |
| Imagens | `ImageField` + Pillow; armazenamento via `STORAGES` do Django | Local em dev; em produção, disco da VPS ou S3-compatível (`django-storages`) sem mudar código |
| Pagamentos | **A definir** (Mercado Pago, Stripe, Pagar.me…) | Isolado atrás de uma interface em `apps/doacoes/gateways/` |
| API (quando precisar) | Django REST Framework, em `/api/v1/` | Só se houver consumidor real (app, integração) |
| Config | `django-environ` + arquivo `.env` | Nada de segredo no código |
| Deploy | Ainda não decidido (VPS, domínio) | Manter tudo configurável por variável de ambiente |

Por que Django e não FastAPI/Flask: login, permissões, formulários, upload de imagens e
edição de conteúdo por pessoas não técnicas (o admin vira o painel do movimento) já vêm
prontos. FastAPI exigiria montar auth, admin e migrations à mão.

## Arquitetura

Um **app Django por domínio**. Uma feature nova vira um app novo, não um arquivo gigante.

```
habonim-dror-brasil/
├── config/                  # projeto Django
│   ├── settings/
│   │   ├── base.py          # comum a todos os ambientes
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── apps/
│   ├── core/                # home, layout base, páginas institucionais, context processors
│   ├── contas/              # User customizado, login/cadastro, perfil
│   ├── movimento/           # pilares, história (timeline), Torá Educativa, shichvot/tochniot
│   ├── snifim/              # snifim, galeria, foto da Bagrut, kehilot parceiras, CCHDs
│   ├── doacoes/             # doações, ranking, integração com gateway de pagamento
│   └── glossario/           # termos em hebraico + definição
│   # futuros: censo/, depoimentos/
├── templates/               # base.html + parciais compartilhadas
├── static/
├── media/                   # uploads em dev (fora do git)
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
└── manage.py
```

### Regras gerais

- **Conteúdo vem do banco, não do template.** Snifim, pilares, tochniot, glossário, números
  e timeline são models editáveis pelo admin. Texto fixo no HTML só para frases de layout.
- Os números do movimento (400 chaverim por semana, 200 por machané, 60 aliot, 25 na Shnat)
  mudam com o tempo, então ficam no banco.
- Cada app tem seu próprio `urls.py` com `app_name` e é incluído em `config/urls.py`.
- Lógica de negócio fica em `services.py` e consultas reaproveitáveis em `selectors.py`.
  As views são finas.
- Slugs em URLs públicas (`/snifim/recife/`), nunca IDs.
- Toda feature nova tem testes (`pytest` + `pytest-django`).

### Contas: anônimo e logado

- **Custom user (`apps/contas.User`, com `AUTH_USER_MODEL`) criado ANTES da primeira migration.**
  Trocar depois é muito difícil.
- **Duas opções explícitas na entrada do site: "Entrar" (login/cadastro) e "Continuar sem
  login".** A escolha anônima é lembrada na sessão (não perguntar de novo a cada página).
  O botão "Entrar" fica sempre visível no cabeçalho para quem escolheu seguir sem login.
- A tela de escolha **não bloqueia o conteúdo**: links diretos (`/snifim/recife/`, vindos do
  Instagram ou do Google) abrem a página normalmente. Bloquear prejudicaria o SEO e quem chega
  por link.
- Login por **e-mail** (não por username).
- Nenhuma página institucional exige login. Visitante anônimo navega e **pode doar** sem conta.
- Permissões por grupo do Django: ex. `editor_nacional` (edita tudo) e `editor_snif` (edita só
  o próprio snif). Modelar a ligação usuário ↔ snif para isso desde o início.

### Snifim

Cada snif tem uma página própria: **`/snifim/<slug>/`** (ex. `/snifim/porto-alegre/`), e uma
listagem em `/snifim/`.

Model `Snif` (base, extensível):
- `nome`, `slug`, `cidade`, `estado`, `ano_fundacao`
- `historia` (texto longo, formatado), `resumo` (para cards da listagem)
- `instagram`, `contato` (e-mail/WhatsApp, opcional), `endereco` (opcional)
- `kehila_parceira` (FK para `Kehila`), `tem_cchd` (+ dados da CCHD quando houver)
- `foto_capa`
- `ativo` (para esconder sem apagar)

Models relacionados:
- `FotoSnif`: galeria (`snif` FK, `imagem`, `legenda`, `ordem`, `data`)
- `Bagrut`: o grupo que gerencia o snif **em um período** (`snif` FK, `ano`/`gestao`, `foto`,
  `descricao`, `atual: bool`). Guardar histórico de Bagrutot; a página mostra a atual.
  Membros com nome/tafkid ficam opcionais (são menores de idade em muitos casos; ver Privacidade).
- `Kehila`: comunidade parceira (`nome`, `cidade`, `site`)

Imagens: validar tipo e tamanho no upload, gerar versão redimensionada/miniatura, sempre com
`alt` preenchido (texto alternativo para acessibilidade).

### Doações

- App `doacoes`, sem carrinho nem produto: **é doação, não loja**.
- Model `Doacao`: `valor` (`DecimalField`, nunca float), `moeda`, `status`
  (`pendente` / `confirmada` / `cancelada` / `estornada`), `usuario` (FK **opcional**),
  `nome_exibicao`, `email` (opcional), `anonima: bool`, `destino` (geral, snif específico,
  bolsas Shnat/machané), `gateway`, `gateway_id`, `created_at`.
- **Doação anônima sempre disponível**, para visitante sem login e para usuário logado. A doação
  anônima nunca aparece no ranking nem expõe nome ou e-mail em lugar público.
- **Ranking**: soma só doações `confirmada` e `anonima=False`. Entrar no ranking é uma
  **escolha explícita** do doador (opt-in), nunca o padrão. Calcular via `selectors.py`
  (agregação no Postgres); cachear se ficar pesado.
- Status só muda para `confirmada` pelo **webhook do gateway** (verificando a assinatura),
  nunca pelo retorno do navegador.
- Gateway atrás de uma interface (`gateways/base.py` + uma implementação por provedor), para
  trocar de provedor sem mexer no resto.
- Nenhum dado de cartão passa pelo nosso servidor: o checkout é do gateway.

### Privacidade (LGPD)

- Muitos chanichim e madrichim são **menores de idade**. Fotos de Bagrut e galeria só sobem
  com autorização; nomes de menores são opcionais e escondidos por padrão.
- O doador controla a própria exposição (anônimo / aparecer no ranking).
- Coletar só os dados necessários. O e-mail do doador nunca é público.

## Convenções

- Código em **português sem acento** para domínio (`Snif`, `Pilar`, `Tochnit`, `Doacao`) e
  inglês para termos técnicos (`created_at`, `is_active`).
- Texto exibido ao usuário em **português do Brasil**.
- Termos em hebraico seguem a grafia do material oficial (tnuá, snif/snifim, chanich/chanichim,
  madrich/madrichim, machané/machanot, peulá/peulot, kehilá/kehilot, shichvá/shichavot).
- **Sempre que um termo do glossário aparecer no texto, ele deve poder mostrar a definição**
  (tooltip/link para o glossário). Isso é importante: o público-alvo não conhece os termos.
- Sem acento em nomes de pasta e arquivo.
- Linguagem de gênero do material: `chaver(á)`, `madrich(á)`.
- Formatação: `ruff` (lint + format).

## Comandos

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements/dev.txt
copy .env.example .env            # e preencher (DATABASE_URL, DJANGO_SECRET_KEY)
python manage.py migrate          # cria tabelas E carrega o conteúdo inicial
python manage.py createsuperuser  # pede e-mail e senha (acesso ao /admin/)
python manage.py runserver
pytest
ruff check . && ruff format .
```

Na máquina de desenvolvimento atual, o Postgres 18 roda na porta **5433** (o 16 está na 5432).

## Como o código está organizado (fase 1 pronta)

- **Textos institucionais** ficam no model `core.BlocoTexto`, buscados por `chave` via
  `apps.core.selectors.blocos(...)`. No template: `{% include "includes/secao.html" with bloco=blocos.x %}`.
  **Bloco com texto vazio não aparece no site**: é assim que pendências (Censo, conta
  nacional) ficam escondidas até alguém preencher pelo admin.
- **Glossário automático**: o filtro `{{ texto|com_glossario }}` (`apps/glossario/services.py`)
  escapa o HTML, cria parágrafos e liga a 1ª ocorrência de cada termo à definição. As formas
  reconhecidas vêm do campo `variantes` de cada `Termo`.
- **Conteúdo inicial** está nas migrations `000X_conteudo_inicial.py` de cada app. Elas só criam
  o que não existe (`get_or_create`), então nunca sobrescrevem edições feitas no admin.
- **Entrada**: `apps/contas/services.py` guarda na sessão a escolha "continuar sem login";
  `ja_escolheu_entrada` fica disponível em todo template via `apps.core.context_processors.site`.
- Templates de cada app ficam em `apps/<app>/templates/<app>/`; os compartilhados, em
  `templates/` (`base.html`, `includes/`). CSS em `static/css/site.css`, com as cores em
  variáveis no topo.
- WhiteNoise (arquivos estáticos) só é ligado em `settings/prod.py`.

URLs atuais: `/`, `/bases/`, `/shichavot-tzeirot/`, `/shichavot-bogrot/`, `/kehila-hd/`,
`/glossario/`, `/quero-saber-mais/`, `/contas/entrar/`, `/contas/sair/`, `/contas/sem-login/`,
`/admin/`.

## Contexto do movimento (resumo do material oficial)

Fonte: `Material HDBR.pdf` (material de divulgação, outubro de 2026).

### Estrutura de páginas

1. **Bases**: quem somos; os 4 pilares; ideologia em movimento; história; Torá Educativa; Dror
   no Brasil hoje; parceiros (kehilot e CCHDs)
2. **ST, Shichavot Tzeirot** (de Chalutzim até Solelim Beit): sábados de atividade, machanot locais
3. **SB, Shichavot Bogrot** (a partir do 9º ano): Projeto Hagshem, temas das tochniot,
   machanot centrais, Shnat Hachshará
4. **Kehilá HD**: formação de liderança (depoimentos), CCHDs, importância do movimento juvenil,
   Censo, Vinho Guefen (só informativo)
5. **Snifim**: listagem + página de cada snif
6. **Doe**: área de doações + ranking
7. **Glossário**
8. **Quero saber mais**: Instagram de cada snif (é a ação final do site)

### Os 4 pilares
- **Judaísmo Cultural Humanista**: tradição judaica centrada no ser humano, plural.
- **Sionismo Socialista**: autodeterminação do povo judeu + sociedade justa e igualitária;
  relação crítica e responsável com Israel.
- **Chalutzianismo (Pioneirismo)**: transformar valores em prática, liderar pelo exemplo.
- **Kibutzianismo (Coletividade)**: cooperação e vida comunitária, no campo ou na cidade,
  em Israel ou na diáspora.

### Snifim (ano de fundação)
Curitiba 1945 · Porto Alegre 1945 · São Paulo 1948 · Rio de Janeiro 1948 · Recife 1957 ·
Bahia (Salvador) 1958 · Belo Horizonte 1982 · Campinas 1996 · Manaus 2009 · Fortaleza 2013.
CCHDs (Casas de Cultura Habonim Dror): Rio de Janeiro, São Paulo e Porto Alegre.

Kehilot parceiras citadas: Sociedade Israelita do Ceará (Fortaleza), Federação Israelita de
Pernambuco (Recife), Sociedade Israelita da Bahia, Federação Israelita do Estado de Minas Gerais
(BH), Sociedade Israelita Brasileira Beth Jacob (Campinas), Centro Israelita do Paraná (Curitiba).

### Tochniot (jornada do Projeto Hagshem)
Solelim Beit → Bonim → Mordim → Maapilim → Magshimim → Shnat → Bagrut (atua como madrich e
gerencia o snif).

### Números
10 snifim · mais de 15 países na rede internacional · cerca de 400 chaverim por semana · cerca de 200 por
machané central · 60 aliot em 10 anos · média de 25 jovens por ano na Shnat.

### Para que servem as doações (do material)
Sustentar a rede de 10 snifim, a Shnat anual, as machanot centrais e a formação de madrichim,
principalmente via **bolsas**. O objetivo é que nenhum jovem deixe de ir a uma machané ou à
Shnat por questão financeira.

### Pendências de conteúdo (usar placeholder até chegar)
- Instagram de cada snif e da conta nacional, mais o link do site oficial
- História, fotos e foto da Bagrut de cada snif
- 3 depoimentos (ex-chaver, madrich atual, kehilá parceira)
- Texto e mecanismo do **Censo**
- Gateway de pagamento e conta que recebe as doações (CNPJ do movimento?)

## Roadmap

- [x] **Fase 1**: setup (Django + Postgres + custom user), páginas institucionais, glossário,
      Quero saber mais, entrada com "Entrar" / "Continuar sem login", login por e-mail
- [ ] **Fase 2**: páginas dos snifim (galeria, Bagrut, história) editáveis pelo admin
- [ ] **Fase 3**: login/cadastro, permissões por snif
- [ ] **Fase 4**: doações (anônima + logada), webhook do gateway, ranking
- [ ] Futuro: Censo, depoimentos enviados pelo site, API pública se necessário
- [ ] Infra: escolher domínio e VPS; HTTPS; backups do Postgres e da pasta de mídia
