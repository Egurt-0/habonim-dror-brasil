"""Apaga dados pessoais que já passaram do prazo de guarda (LGPD).

Rodar uma vez por dia no servidor (cron), ex.: python manage.py limpar_dados_pessoais
"""

from django.core.management import BaseCommand, call_command

from apps.contas.services import (
    RETENCAO_REGISTROS_DIAS,
    apagar_cadastros_pendentes_antigos,
    apagar_registros_de_acesso_antigos,
)


class Command(BaseCommand):
    help = (
        "Apaga registros de login antigos, cadastros pendentes vencidos e sessões expiradas (LGPD)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dias", type=int, default=RETENCAO_REGISTROS_DIAS)

    def handle(self, *args, dias, **options):
        apagados = apagar_registros_de_acesso_antigos(dias)
        cadastros = apagar_cadastros_pendentes_antigos()
        call_command("clearsessions")
        self.stdout.write(f"{apagados} registros de login com mais de {dias} dias apagados.")
        self.stdout.write(f"{cadastros} cadastros pendentes vencidos apagados.")
