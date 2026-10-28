import pytest
from django.core.exceptions import ValidationError

from apps.core.models import Topico


def _topico(link):
    return Topico(titulo="x", slug="x", resumo="x", link=link)


@pytest.mark.django_db
@pytest.mark.parametrize("link", ["javascript:alert(1)", "//x.com", "/\\x.com"])
def test_link_externo_ou_de_esquema_perigoso_e_recusado(link):
    with pytest.raises(ValidationError):
        _topico(link).full_clean()


@pytest.mark.django_db
def test_link_interno_e_aceito():
    _topico("/bases/#pilares").full_clean()
