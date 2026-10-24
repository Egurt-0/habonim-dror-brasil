"""Política de privacidade: cadastro só para maiores de 18 e registro do aceite (fase 3).

Só troca o trecho se ele ainda estiver igual ao original (não mexe em edição do admin).
"""

from django.db import migrations

ANTIGO = (
    "Conta (opcional): e-mail, nome e senha, guardada de forma criptografada. Servem para "
    "o login e para recursos como o histórico de doações. Base legal: execução do serviço "
    "que você pediu."
)
NOVO = (
    "Conta (opcional e só para maiores de 18 anos): nome, e-mail e senha, guardada de forma "
    "criptografada, além da data em que você aceitou esta política e declarou ter 18 anos "
    "ou mais. Servem para o login e para recursos como o histórico de doações. Base legal: "
    "execução do serviço que você pediu. Na página “Meus dados” você pode ver, corrigir, "
    "baixar e excluir esses dados."
)


def _trocar(apps, de, para):
    BlocoTexto = apps.get_model("core", "BlocoTexto")
    for bloco in BlocoTexto.objects.filter(chave="priv_dados", texto__contains=de):
        bloco.texto = bloco.texto.replace(de, para)
        bloco.save(update_fields=["texto"])


def aplicar(apps, schema_editor):
    _trocar(apps, ANTIGO, NOVO)


def desfazer(apps, schema_editor):
    _trocar(apps, NOVO, ANTIGO)


class Migration(migrations.Migration):
    dependencies = [("core", "0008_politica_de_privacidade")]

    operations = [migrations.RunPython(aplicar, desfazer)]
