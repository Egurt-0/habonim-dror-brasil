"""Tópicos iniciais da grade da home. Depois, editados pelo admin."""

from django.db import migrations

TOPICOS = [
    # (slug, título, resumo, link)
    (
        "quem-somos",
        "Quem somos",
        "O maior movimento juvenil judaico do Brasil, presente no país desde 1945.",
        "/bases/#quem-somos",
    ),
    (
        "pilares",
        "Os quatro pilares",
        "Judaísmo humanista, sionismo socialista, chalutzianismo e kibutzianismo.",
        "/bases/#pilares",
    ),
    (
        "historia",
        "80 anos de história",
        "De Curitiba e Porto Alegre em 1945 a Fortaleza em 2013: 10 snifim pelo Brasil.",
        "/bases/#historia",
    ),
    (
        "shichavot-tzeirot",
        "Shichavot Tzeirot",
        "Os mais novos: peulot todo sábado e machanot locais.",
        "/shichavot-tzeirot/",
    ),
    (
        "shichavot-bogrot",
        "Shichavot Bogrot",
        "A partir do 9º ano, quem foi educado passa a educar.",
        "/shichavot-bogrot/",
    ),
    (
        "shnat",
        "Shnat Hachshará",
        "Um ano de formação intensiva em Israel.",
        "/shichavot-bogrot/#shnat",
    ),
    (
        "kehila-hd",
        "Kehilá HD",
        "Lideranças formadas na tnuá que sustentam as comunidades.",
        "/kehila-hd/",
    ),
    (
        "contribua",
        "Contribua",
        "Bolsas para que nenhum jovem fique de fora de uma machané ou da Shnat.",
        "/kehila-hd/#contribua",
    ),
    (
        "snifim",
        "Encontre seu snif",
        "Fale com o Habonim Dror da sua cidade.",
        "/quero-saber-mais/",
    ),
]


def criar_topicos(apps, schema_editor):
    Topico = apps.get_model("core", "Topico")
    for ordem, (slug, titulo, resumo, link) in enumerate(TOPICOS):
        Topico.objects.get_or_create(
            slug=slug,
            defaults={"titulo": titulo, "resumo": resumo, "link": link, "ordem": ordem},
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0003_topico")]

    operations = [migrations.RunPython(criar_topicos, migrations.RunPython.noop)]
