"""Glossário inicial, do Material HDBR (outubro de 2026), mais alguns termos usados no texto.

Termos que não estão no material, mas aparecem no texto: boguer, tochnit, bagrut, tafkid,
tzevet, kibutz e CCHD.
"""

from django.db import migrations

TERMOS = [
    # (termo, slug, definição, variantes)
    ("Tnuá", "tnua", "Movimento juvenil.", "tnuá, tnuot"),
    ("Snif", "snif", "Núcleo local do movimento em uma cidade.", "snif, snifim"),
    ("Kehilá", "kehila", "Comunidade judaica local.", "kehilá, kehilot"),
    ("Chaver(á)", "chaver", "Integrante do movimento.", "chaver, chaverá, chaverim"),
    (
        "Chanich(á)",
        "chanich",
        "Educando(a) e participante das atividades.",
        "chanich, chanichá, chanichim",
    ),
    (
        "Madrich(á)",
        "madrich",
        "Educador(a) voluntário(a) do movimento.",
        "madrich, madrichá, madrichim",
    ),
    ("Peulá", "peula", "Atividade educativa.", "peulá, peulot"),
    ("Kvutzá", "kvutza", "Grupo de chaverim.", "kvutzá, kvutzot"),
    ("Shichvá", "shichva", "Grupo etário nacional.", "shichvá, shichavot"),
    (
        "Machané / Kaitaná",
        "machane",
        "Acampamento de imersão.",
        "machané, machanot, kaitaná",
    ),
    ("Hadrachá", "hadracha", "Formação e prática de liderança educacional.", "hadrachá"),
    ("Shnat Hachshará", "shnat", "Ano de formação em Israel.", "Shnat Hachshará, Shnat"),
    (
        "Hagshamá",
        "hagshama",
        "Realização prática dos valores da tnuá, na diáspora ou por meio da aliá.",
        "hagshamá",
    ),
    (
        "Aliá Chalutziana",
        "alia",
        "Imigração para Israel com propósito de construção social.",
        "aliá chalutziana, aliá, aliot",
    ),
    ("Mazkir(á)", "mazkir", "Direção ou secretaria geral, nacional ou local.", "mazkir, mazkirá"),
    ("Guizbar(it)", "guizbar", "Tesoureiro(a), nacional ou local.", "guizbar, guizbarit"),
    ("Rakaz(et) Chinuch", "rakaz-chinuch", "Coordenador(a) pedagógico(a).", "rakaz, rakezet"),
    ("Hanagá Artzit", "hanaga-artzit", "Liderança nacional do movimento.", "hanagá artzit"),
    (
        "Veidá",
        "veida",
        "Congresso ou assembleia máxima da tnuá, realizado a cada dois anos.",
        "veidá",
    ),
    (
        "Dugmá Ishit",
        "dugma-ishit",
        "Exemplo pessoal, um dos pilares da educação da tnuá.",
        "dugmá ishit",
    ),
    # Não estão no glossário do material, mas aparecem no texto do site.
    (
        "Boguer(et)",
        "boguer",
        "Chaver(á) mais velho(a), das Shichavot Bogrot em diante.",
        "boguer, bogeret, bogrim",
    ),
    ("Tochnit", "tochnit", "Programação educacional de uma etapa da tnuá.", "tochnit, tochniot"),
    (
        "Bagrut",
        "bagrut",
        "Etapa final da jornada: o boguer atua como madrich e participa da gestão do snif.",
        "bagrut",
    ),
    ("Tafkid", "tafkid", "Função ou responsabilidade assumida na tnuá.", "tafkid, tafkidim"),
    ("Tzevet", "tzevet", "Equipe.", "tzevet"),
    (
        "Kibutz",
        "kibutz",
        "Comunidade coletiva em Israel, baseada na cooperação e na vida comunitária.",
        "kibutz, kibutzim",
    ),
    (
        "CCHD",
        "cchd",
        "Casa de Cultura Habonim Dror: espaço próprio da tnuá em uma cidade.",
        "CCHD, CCHDs",
    ),
]


def criar_termos(apps, schema_editor):
    Termo = apps.get_model("glossario", "Termo")
    for termo, slug, definicao, variantes in TERMOS:
        Termo.objects.get_or_create(
            slug=slug, defaults={"termo": termo, "definicao": definicao, "variantes": variantes}
        )


class Migration(migrations.Migration):
    dependencies = [("glossario", "0001_initial")]

    operations = [migrations.RunPython(criar_termos, migrations.RunPython.noop)]
