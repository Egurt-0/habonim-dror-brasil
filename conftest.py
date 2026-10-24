import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def _cache_limpo():
    """O rollback do banco entre testes não dispara sinais; limpar o cache evita vazamento."""
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def painel(client):
    """Loga no painel como `user`, já passando pela verificação em duas etapas."""
    from django_otp import DEVICE_ID_SESSION_KEY
    from django_otp.plugins.otp_static.models import StaticDevice

    def entrar(user):
        device = StaticDevice.objects.create(user=user, name="teste", confirmed=True)
        client.force_login(user)
        sessao = client.session
        sessao[DEVICE_ID_SESSION_KEY] = device.persistent_id
        sessao.save()
        return client

    return entrar
