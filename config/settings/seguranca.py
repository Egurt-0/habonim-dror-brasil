"""Checagens que impedem o site de subir em produção com configuração insegura."""

TAMANHO_MINIMO_CHAVE = 50


def chave_secreta_fraca(chave):
    """True para a chave de exemplo do .env.example, a padrão do Django ou uma chave curta."""
    return (
        chave.startswith(("troque", "django-insecure"))
        or len(chave) < TAMANHO_MINIMO_CHAVE
        or len(set(chave)) < 10
    )
