"""Dados fixos do movimento usados em vários textos do site."""

from django.utils import timezone

ANO_FUNDACAO = 1945  # chegada do Habonim Dror ao Brasil

# Escrito em um texto do admin, vira a idade do movimento (ex.: "{anos} anos de história").
MARCADOR_ANOS = "{anos}"


def anos_de_movimento(hoje=None):
    hoje = hoje or timezone.localdate()
    return hoje.year - ANO_FUNDACAO


def com_anos(texto):
    """Troca o marcador {anos} pela idade do movimento no ano atual."""
    if not texto or MARCADOR_ANOS not in texto:
        return texto
    return texto.replace(MARCADOR_ANOS, str(anos_de_movimento()))
