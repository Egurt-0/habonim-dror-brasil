from .models import Numero, Pilar, ReferenciaPedagogica, Tochnit


def pilares():
    return Pilar.objects.all()


def referencias_pedagogicas():
    return ReferenciaPedagogica.objects.all()


def tochniot():
    return Tochnit.objects.all()


def numeros():
    return Numero.objects.all()


def numeros_em_destaque():
    return Numero.objects.filter(destaque=True)
