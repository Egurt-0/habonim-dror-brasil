# Habonim Dror Brasil — site

Site do **Habonim Dror Brasil (HDBR)**, movimento juvenil judaico (tnuá) sionista socialista,
chalutziano e kibutziano, presente no Brasil desde 1945.

## Objetivo

Fase 1: um site **introdutório** que apresente o movimento para quem não o conhece (pais,
comunidade, possíveis chanichim, parceiros, doadores). O material de divulgação define três
argumentos centrais, que devem guiar texto e layout:

1. **Capilaridade nacional**: não é uma tnuá local, é uma rede que conecta o Brasil inteiro.
2. **Alcance**: chega a crianças sem escola judaica ou outras opções de educação judaica.
3. **Impacto comunitário**: forma as lideranças que sustentam as pequenas comunidades.

Slogan: **"80 anos formando líderes, construindo comunidade e conectando gerações."**

O site vai crescer (usuários logados e anônimos, censo, contribuições, venda de vinho etc.).
**Toda decisão deve facilitar adicionar features depois**, sem reescrever o que existe.

## Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Linguagem | Python 3.12 | O dono do projeto mexe com Python com mais segurança |
| Framework | **Django 5.2 LTS** | Auth, admin, ORM, migrations, forms e CSRF prontos; suporte até 2028 |
| Front | Templates Django + CSS próprio; **HTMX** quando precisar de interatividade | Sem build de JS, sem SPA |
| API (quando precisar) | Django REST Framework, em `/api/v1/` | Só se houver consumidor real (app, integração) |
| Banco | SQLite em dev → PostgreSQL em produção | Ainda não decidido; o código não pode depender de um banco específico |
| Config | `django-environ` + arquivo `.env` | Nada de segredo no código |
| Deploy | Ainda não decidido (VPS, domínio) | Manter tudo configurável por variável de ambiente |

Por que Django e não FastAPI/Flask: o roadmap inclui contas de usuário, permissões, formulários
e edição de conteúdo por pessoas não técnicas. O Django já traz isso tudo (o admin vira o
painel de conteúdo do movimento). FastAPI exigiria montar auth, admin e migrations à mão.

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
│   ├── movimento/           # pilares, história (timeline), Torá Educativa, shichvot/tochniot
│   ├── snifim/              # snifim, kehilot parceiras, CCHDs, Instagram de cada snif
│   └── glossario/           # termos em hebraico + definição
│   # futuros: contas/, censo/, contribuicoes/, loja/ (Vinho Guefen), depoimentos/
├── templates/               # base.html + parciais compartilhadas
├── static/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env.example
└── manage.py
```

### Regras

- **Conteúdo vem do banco, não do template.** Snifim, pilares, tochniot, glossário, números
  e timeline são models editáveis pelo admin. Texto fixo no HTML só para frases de layout.
- Os números do movimento (400 chaverim por semana, 200 por machané, 60 aliot, 25 na Shnat)
  mudam com o tempo, então ficam no banco.
- Cada app tem seu próprio `urls.py` com `app_name` e é incluído em `config/urls.py`.
- Lógica de negócio fica em `services.py` e consultas reaproveitáveis em `selectors.py`.
  As views são finas.
- Pensar desde já em **anônimo vs. logado**: as páginas da fase 1 são públicas. Quando entrarem
  contas, usar um `User` customizado (`apps/contas`). **Criar o custom user ANTES da primeira
  migration**, porque trocar depois é doloroso. Ou seja, o app `contas` com
  `AUTH_USER_MODEL` entra já no setup inicial, mesmo vazio.
- Slugs em URLs públicas (`/snifim/recife/`), nunca IDs.
- Toda feature nova tem testes (`pytest` + `pytest-django`).

## Convenções

- Código (nomes de variáveis, funções, models) em **inglês ou português sem acento**; escolher
  um e manter. Padrão adotado: **português sem acento** para domínio (`Snif`, `Pilar`,
  `Tochnit`) e inglês para termos técnicos (`created_at`, `is_active`).
- Texto exibido ao usuário em **português do Brasil**.
- Termos em hebraico seguem a grafia do material oficial (tnuá, snif/snifim, chanich/chanichim,
  madrich/madrichim, machané/machanot, peulá/peulot, kehilá/kehilot, shichvá/shichavot).
- **Sempre que um termo do glossário aparecer no texto, ele deve poder mostrar a definição**
  (tooltip/link para o glossário). Isso é importante: o público-alvo não conhece os termos.
- Sem acento em nomes de pasta e arquivo.
- Linguagem de gênero do material: `chaver(á)`, `madrich(á)`.
- Formatação: `ruff` (lint + format).

## Comandos

> Ainda não existe código. Atualizar esta seção quando o projeto for criado.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver
pytest
ruff check . && ruff format .
```

## Contexto do movimento (resumo do material oficial)

Fonte: `Material HDBR.pdf` (material de divulgação, outubro de 2026).

### Estrutura de páginas da fase 1

1. **Bases**: quem somos; os 4 pilares; ideologia em movimento; história; Torá Educativa; Dror
   no Brasil hoje; parceiros (kehilot e CCHDs)
2. **ST, Shichavot Tzeirot** (de Chalutzim até Solelim Beit): sábados de atividade, machanot locais
3. **SB, Shichavot Bogrot** (a partir do 9º ano): Projeto Hagshem, temas das tochniot,
   machanot centrais, Shnat Hachshará
4. **Kehilá HD**: formação de liderança (depoimentos), CCHDs, importância do movimento juvenil,
   Contribua, Censo, Vinho Guefen
5. **Glossário**
6. **Quero saber mais**: Instagram de cada snif (é a ação final do site)

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
Solelim Beit → Bonim → Mordim → Maapilim → Magshimim → Shnat → Bagrut (atua como madrich).

### Números
10 snifim · mais de 15 países na rede internacional · cerca de 400 chaverim por semana · cerca de 200 por
machané central · 60 aliot em 10 anos · média de 25 jovens por ano na Shnat.

### Pendências de conteúdo (usar placeholder até chegar)
- Instagram de cada snif e da conta nacional, mais o link do site oficial
- 3 depoimentos (ex-chaver, madrich atual, kehilá parceira)
- Texto e mecanismo do **Censo**
- Como contribuir (PIX, link, formulário) e como comprar o **Vinho Guefen**

## Roadmap

- [ ] **Fase 1**: site introdutório público (páginas acima + glossário + Quero saber mais)
- [ ] Fase 2: contas de usuário (custom user, login), áreas para logados
- [ ] Futuro: Censo, Contribua (bolsas), Vinho Guefen (pedidos), depoimentos enviados pelo site
- [ ] Infra: escolher domínio, VPS e banco; HTTPS; backups
