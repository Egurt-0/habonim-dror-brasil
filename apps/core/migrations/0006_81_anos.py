"""O movimento completou 81 anos: atualiza os textos iniciais que ainda diziam 80.

Só troca o texto que continua igual ao original (não mexe em edição feita no admin).
"""

from django.db import migrations

# (model, campo de busca, valor, campo do texto, texto antigo, texto novo)
TROCAS = [
    (
        "BlocoTexto",
        "chave",
        "home_hero",
        "texto",
        "Uma rede nacional de educação judaica não formal, com 80 anos de história no Brasil.",
        "Uma rede nacional de educação judaica não formal, com 81 anos de história no Brasil.",
    ),
    (
        "BlocoTexto",
        "chave",
        "slogan",
        "titulo",
        "80 anos formando líderes, construindo comunidade e conectando gerações.",
        "81 anos formando líderes, construindo comunidade e conectando gerações.",
    ),
    ("Topico", "slug", "historia", "titulo", "80 anos de história", "81 anos de história"),
]

TRECHO_HISTORIA = ("Oitenta anos depois", "Oitenta e um anos depois")


def _aplicar(apps, de, para):
    for model, campo, valor, campo_texto, antigo, novo in TROCAS:
        textos = {"antigo": antigo, "novo": novo}
        apps.get_model("core", model).objects.filter(
            **{campo: valor, campo_texto: textos[de]}
        ).update(**{campo_texto: textos[para]})

    BlocoTexto = apps.get_model("core", "BlocoTexto")
    trecho_de, trecho_para = TRECHO_HISTORIA if de == "antigo" else TRECHO_HISTORIA[::-1]
    for bloco in BlocoTexto.objects.filter(chave="historia", texto__contains=trecho_de):
        bloco.texto = bloco.texto.replace(trecho_de, trecho_para)
        bloco.save(update_fields=["texto"])


def aplicar(apps, schema_editor):
    _aplicar(apps, "antigo", "novo")


def desfazer(apps, schema_editor):
    _aplicar(apps, "novo", "antigo")


class Migration(migrations.Migration):
    dependencies = [("core", "0005_snifim_intro_e_topico")]

    operations = [migrations.RunPython(aplicar, desfazer)]
