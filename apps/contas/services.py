"""Escolha de entrada: o visitante entra com login ou segue sem login."""

SESSION_KEY_SEM_LOGIN = "seguir_sem_login"


def escolher_seguir_sem_login(request):
    request.session[SESSION_KEY_SEM_LOGIN] = True


def ja_escolheu_entrada(request):
    """True se o visitante está logado ou já escolheu seguir sem login."""
    return request.user.is_authenticated or request.session.get(SESSION_KEY_SEM_LOGIN, False)
