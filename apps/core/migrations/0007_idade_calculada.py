"""A idade do movimento passa a ser calculada pelo ano (marcador {anos}), sem precisar
trocar o número todo ano.

Só troca o texto que continua igual ao da migration 0006 (não mexe em edição do admin).
"""

from django.db import migrations

# (model, campo de busca, valor, campo do texto, texto fixo, texto com marcador)
TROCAS = [
    (
        "BlocoTexto",
        "chave",
        "home_hero",
        "texto",
        "Uma rede nacional de educação judaica não formal, com 81 anos de história no Brasil.",
        "Uma rede nacional de educação judaica não formal, com {anos} anos de história no Brasil.",
    ),
    (
        "BlocoTexto",
        "chave",
        "slogan",
        "titulo",
        "81 anos formando líderes, construindo comunidade e conectando gerações.",
        "{anos} anos formando líderes, construindo comunidade e conectando gerações.",
    ),
    ("Topico", "slug", "historia", "titulo", "81 anos de história", "{anos} anos de história"),
]

TRECHO_HISTORIA = ("Oitenta e um anos depois", "{anos} anos depois")


def _aplicar(apps, de, para):
    for model, campo, valor, campo_texto, fixo, marcador in TROCAS:
        textos = {"fixo": fixo, "marcador": marcador}
        apps.get_model("core", model).objects.filter(
            **{campo: valor, campo_texto: textos[de]}
        ).update(**{campo_texto: textos[para]})

    BlocoTexto = apps.get_model("core", "BlocoTexto")
    trecho_de, trecho_para = TRECHO_HISTORIA if de == "fixo" else TRECHO_HISTORIA[::-1]
    for bloco in BlocoTexto.objects.filter(chave="historia", texto__contains=trecho_de):
        bloco.texto = bloco.texto.replace(trecho_de, trecho_para)
        bloco.save(update_fields=["texto"])


def aplicar(apps, schema_editor):
    _aplicar(apps, "fixo", "marcador")


def desfazer(apps, schema_editor):
    _aplicar(apps, "marcador", "fixo")


class Migration(migrations.Migration):
    dependencies = [("core", "0006_81_anos")]

    operations = [migrations.RunPython(aplicar, desfazer)]
