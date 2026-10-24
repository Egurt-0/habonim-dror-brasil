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
    """Loga no painel como `user` (já passando pela verificação em duas etapas, se houver)."""

    def entrar(user):
        client.force_login(user)
        return client

    return entrar
