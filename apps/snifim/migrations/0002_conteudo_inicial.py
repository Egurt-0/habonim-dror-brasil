"""Os 10 snifim e as kehilot parceiras citadas no Material HDBR (outubro de 2026).

Instagram de cada snif ainda pendente: preencher pelo admin.
"""

from django.db import migrations

KEHILOT = {
    "ceara": ("Sociedade Israelita do Ceará", "Fortaleza"),
    "pernambuco": ("Federação Israelita de Pernambuco", "Recife"),
    "bahia": ("Sociedade Israelita da Bahia", "Salvador"),
    "minas": ("Federação Israelita do Estado de Minas Gerais", "Belo Horizonte"),
    "campinas": ("Sociedade Israelita Brasileira Beth Jacob", "Campinas"),
    "parana": ("Centro Israelita do Paraná", "Curitiba"),
}

SNIFIM = [
    # (nome, slug, cidade, UF, ano de fundação, kehilá, tem CCHD)
    ("Curitiba", "curitiba", "Curitiba", "PR", 1945, "parana", False),
    ("Porto Alegre", "porto-alegre", "Porto Alegre", "RS", 1945, None, True),
    ("São Paulo", "sao-paulo", "São Paulo", "SP", 1948, None, True),
    ("Rio de Janeiro", "rio-de-janeiro", "Rio de Janeiro", "RJ", 1948, None, True),
    ("Recife", "recife", "Recife", "PE", 1957, "pernambuco", False),
    ("Bahia", "bahia", "Salvador", "BA", 1958, "bahia", False),
    ("Belo Horizonte", "belo-horizonte", "Belo Horizonte", "MG", 1982, "minas", False),
    ("Campinas", "campinas", "Campinas", "SP", 1996, "campinas", False),
    ("Manaus", "manaus", "Manaus", "AM", 2009, None, False),
    ("Fortaleza", "fortaleza", "Fortaleza", "CE", 2013, "ceara", False),
]


def criar_snifim(apps, schema_editor):
    Kehila = apps.get_model("snifim", "Kehila")
    Snif = apps.get_model("snifim", "Snif")

    kehilot = {}
    for chave, (nome, cidade) in KEHILOT.items():
        kehilot[chave], _ = Kehila.objects.get_or_create(nome=nome, defaults={"cidade": cidade})

    for nome, slug, cidade, uf, ano, kehila, cchd in SNIFIM:
        Snif.objects.get_or_create(
            slug=slug,
            defaults={
                "nome": nome,
                "cidade": cidade,
                "estado": uf,
                "ano_fundacao": ano,
                "kehila": kehilot.get(kehila),
                "tem_cchd": cchd,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("snifim", "0001_initial")]

    operations = [migrations.RunPython(criar_snifim, migrations.RunPython.noop)]
