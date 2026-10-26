"""Grupos de permissão do painel, definidos aqui no código (não à mão pelo admin).

- editor_nacional: edita todo o conteúdo do site (textos, glossário, movimento, snifim).
  Não mexe em usuários, grupos nem permissões: isso é só do superusuário.
- editor_snif: só os snifim ligados à própria conta (campo "snifim que edita" do usuário):
  texto, fotos, Bagrut e contato. Não cria nem apaga snif, não vê o resto do site.

As permissões são recriadas a cada `migrate` (sinal post_migrate), então o que vale é o que
está neste arquivo. Mudou um grupo? Mude aqui.
"""

from django.apps import apps as apps_globais

EDITOR_NACIONAL = "editor_nacional"
EDITOR_SNIF = "editor_snif"

TODAS = ["add", "change", "delete", "view"]

# {grupo: {"app.model" ou "app": [ações]}}; "app" sozinho vale para todos os models do app.
GRUPOS = {
    EDITOR_NACIONAL: {
        "core": TODAS,
        "glossario": TODAS,
        "movimento": TODAS,
        "snifim": TODAS,
    },
    EDITOR_SNIF: {
        "snifim.snif": ["view", "change"],
        "snifim.fotosnif": TODAS,
        "snifim.bagrut": TODAS,
    },
}

# Campos que o editor de snif vê mas não altera (identidade e parcerias do snif).
CAMPOS_SO_LEITURA_EDITOR_SNIF = [
    "nome",
    "slug",
    "cidade",
    "estado",
    "ano_fundacao",
    "ativo",
    "ordem",
    "kehila",
    "tem_cchd",
]


def _models(alvo, apps):
    if "." in alvo:
        return [apps.get_model(*alvo.split("."))]
    return list(apps.get_app_config(alvo).get_models())


def garantir_grupos(apps=apps_globais, **kwargs):
    """Cria os grupos e acerta as permissões. Pode rodar quantas vezes for preciso."""
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    for nome, regras in GRUPOS.items():
        codenames = []
        for alvo, acoes in regras.items():
            for model in _models(alvo, apps):
                rotulo = model._meta.model_name
                app_label = model._meta.app_label
                codenames += [(app_label, f"{acao}_{rotulo}") for acao in acoes]
        permissoes = [
            p
            for app_label, codename in codenames
            for p in Permission.objects.filter(content_type__app_label=app_label, codename=codename)
        ]
        grupo, _ = Group.objects.get_or_create(name=nome)
        grupo.permissions.set(permissoes)


def edita_todos_os_snifim(user):
    return user.is_superuser or user.groups.filter(name=EDITOR_NACIONAL).exists()
