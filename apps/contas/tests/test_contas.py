import pytest
from django.urls import reverse

from apps.contas.models import User
from apps.contas.services import SESSION_KEY_SEM_LOGIN


@pytest.mark.django_db
class TestUser:
    def test_cria_usuario_por_email(self):
        user = User.objects.create_user(email="Pessoa@Exemplo.com", password="senha-forte-123")
        assert user.email == "Pessoa@exemplo.com"
        assert user.check_password("senha-forte-123")
        assert not user.is_staff

    def test_email_obrigatorio(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="x")

    def test_superusuario(self):
        admin = User.objects.create_superuser(email="admin@exemplo.com", password="x")
        assert admin.is_staff and admin.is_superuser


@pytest.mark.django_db
class TestEntrada:
    def test_home_mostra_as_duas_opcoes_na_primeira_visita(self, client):
        html = client.get(reverse("core:home")).content.decode()
        assert "Entrar com minha conta" in html
        assert "Continuar sem login" in html

    def test_continuar_sem_login_e_lembrado(self, client):
        resposta = client.post(reverse("contas:sem_login"), {"next": "/bases/"})
        assert resposta.status_code == 302
        assert resposta.url == "/bases/"
        assert client.session[SESSION_KEY_SEM_LOGIN] is True
        html = client.get(reverse("core:home")).content.decode()
        assert "Continuar sem login" not in html

    def test_continuar_sem_login_nao_redireciona_para_fora(self, client):
        resposta = client.post(reverse("contas:sem_login"), {"next": "https://malicioso.com/"})
        assert resposta.url == reverse("core:home")

    def test_continuar_sem_login_exige_post(self, client):
        assert client.get(reverse("contas:sem_login")).status_code == 405

    def test_login_por_email(self, client):
        User.objects.create_user(email="madrich@exemplo.com", password="senha-forte-123")
        resposta = client.post(
            reverse("contas:entrar"),
            {"username": "madrich@exemplo.com", "password": "senha-forte-123"},
        )
        assert resposta.status_code == 302
        html = client.get(reverse("core:home")).content.decode()
        assert "Continuar sem login" not in html
        assert "madrich@exemplo.com" in html

    def test_login_com_senha_errada(self, client):
        User.objects.create_user(email="madrich@exemplo.com", password="senha-forte-123")
        resposta = client.post(
            reverse("contas:entrar"), {"username": "madrich@exemplo.com", "password": "errada"}
        )
        assert resposta.status_code == 200
        assert "E-mail ou senha incorretos" in resposta.content.decode()
