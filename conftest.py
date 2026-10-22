import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def _cache_limpo():
    """O rollback do banco entre testes não dispara sinais; limpar o cache evita vazamento."""
    cache.clear()
    yield
    cache.clear()
