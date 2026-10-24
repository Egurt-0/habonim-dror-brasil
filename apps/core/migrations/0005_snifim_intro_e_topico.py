"""Texto de abertura da página /snifim/ e card "Encontre seu snif" da home apontando para ela.

Como as outras migrations de conteúdo, não sobrescreve o que já foi editado no admin.
"""

from django.db import migrations

INTRO = (
    "Do Sul ao Norte, o Habonim Dror está em 10 cidades brasileiras. Cada snif tem sua "
    "história, sua Bagrut e suas peulot, e todos fazem parte de uma mesma rede nacional.\n\n"
    "Escolha um snif para conhecer sua história e falar com quem está lá."
)


def aplicar(apps, schema_editor):
    BlocoTexto = apps.get_model("core", "BlocoTexto")
    Topico = apps.get_model("core", "Topico")
    BlocoTexto.objects.get_or_create(
        chave="snifim_intro", defaults={"titulo": "Snifim", "texto": INTRO}
    )
    # Só troca o link se ainda for o original (não mexe em edição feita no admin).
    Topico.objects.filter(slug="snifim", link="/quero-saber-mais/").update(link="/snifim/")


def desfazer(apps, schema_editor):
    Topico = apps.get_model("core", "Topico")
    Topico.objects.filter(slug="snifim", link="/snifim/").update(link="/quero-saber-mais/")


class Migration(migrations.Migration):
    dependencies = [("core", "0004_topicos_iniciais")]

    operations = [migrations.RunPython(aplicar, desfazer)]
