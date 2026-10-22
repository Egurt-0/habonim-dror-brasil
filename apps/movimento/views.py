from django.shortcuts import render

from apps.core.selectors import blocos
from apps.snifim.selectors import kehilot_parceiras, linha_do_tempo, snifim_ativos

from . import selectors


def bases(request):
    contexto = {
        "blocos": blocos(
            "quem_somos",
            "pilares_intro",
            "ideologia_em_movimento",
            "historia",
            "tora_educativa",
            "tora_educativa_objetivo",
            "dror_hoje",
            "rede_internacional",
            "parceiros",
            "cchds_parceiros",
        ),
        "pilares": selectors.pilares(),
        "referencias": selectors.referencias_pedagogicas(),
        "numeros": selectors.numeros(),
        "linha_do_tempo": linha_do_tempo(),
        "snifim": snifim_ativos(),
        "kehilot": kehilot_parceiras(),
    }
    return render(request, "movimento/bases.html", contexto)


def shichavot_tzeirot(request):
    contexto = {"blocos": blocos("st_intro", "st_sabados", "st_machanot_locais")}
    return render(request, "movimento/shichavot_tzeirot.html", contexto)


def shichavot_bogrot(request):
    contexto = {
        "blocos": blocos(
            "sb_intro",
            "sb_hagshem",
            "sb_tochniot",
            "sb_tochniot_fecho",
            "sb_machanot_centrais",
            "sb_shnat",
        ),
        "tochniot": selectors.tochniot(),
    }
    return render(request, "movimento/shichavot_bogrot.html", contexto)


def kehila_hd(request):
    contexto = {
        "blocos": blocos(
            "kh_lideranca",
            "kh_cchds",
            "kh_importancia",
            "kh_contribua",
            "kh_censo",
            "kh_vinho",
        ),
    }
    return render(request, "movimento/kehila_hd.html", contexto)
