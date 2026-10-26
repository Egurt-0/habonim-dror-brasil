"""Instagram de cada snif, enviado pelo movimento em outubro de 2026.

Só preenche quem ainda está sem Instagram: nunca sobrescreve o que foi editado no admin.
"""

from django.db import migrations

INSTAGRAM = {
    "curitiba": "drorctba",
    "sao-paulo": "habonimdrorsp",
    "porto-alegre": "habonimdrorpoa",
    "belo-horizonte": "drorsnifbh",
    "rio-de-janeiro": "haborio",
    "recife": "hdsnifrecife",
    "manaus": "hdsnifmanaus",
    "campinas": "drorcampinas",
    "fortaleza": "habonimdrorfortaleza",
    "bahia": "drorzinhoba",
}


def preencher_instagram(apps, schema_editor):
    Snif = apps.get_model("snifim", "Snif")
    for slug, usuario in INSTAGRAM.items():
        Snif.objects.filter(slug=slug, instagram="").update(instagram=usuario)


class Migration(migrations.Migration):
    dependencies = [("snifim", "0004_avisos_lgpd")]

    operations = [migrations.RunPython(preencher_instagram, migrations.RunPython.noop)]
