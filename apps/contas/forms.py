"""Formulários de conta.

Todos são `forms.Form` com lista fechada de campos (nunca ModelForm com "__all__"): um POST
com campos a mais, como is_staff=True, é simplesmente ignorado.
"""

from django import forms
from django.contrib.auth.forms import PasswordResetForm

from . import services


class CadastroForm(forms.Form):
    """Sem senha: ela é criada no link enviado por e-mail, então só o dono do e-mail a define."""

    first_name = forms.CharField(
        label="Nome", max_length=150, widget=forms.TextInput(attrs={"autocomplete": "given-name"})
    )
    email = forms.EmailField(
        label="E-mail", widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )
    maior_de_idade = forms.BooleanField(
        label="Tenho 18 anos ou mais",
        error_messages={"required": "O cadastro é só para maiores de 18 anos."},
    )
    aceite = forms.BooleanField(
        label="Li e aceito a política de privacidade",
        error_messages={"required": "Para criar a conta, aceite a política de privacidade."},
    )


class MeusDadosForm(forms.Form):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=False)


class ExcluirContaForm(forms.Form):
    senha = forms.CharField(
        label="Sua senha, para confirmar",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_senha(self):
        senha = self.cleaned_data["senha"]
        if not self.user.check_password(senha):
            raise forms.ValidationError("Senha incorreta.")
        return senha


class CodigoForm(forms.Form):
    codigo = forms.CharField(
        label="Código",
        max_length=20,
        widget=forms.TextInput(
            attrs={"autocomplete": "one-time-code", "autocapitalize": "off", "spellcheck": "false"}
        ),
    )


class EsqueciSenhaForm(PasswordResetForm):
    """O formulário do Django, com limite de envios por e-mail e link montado com SITE_URL.

    Só manda para contas ativas e com senha (regra do próprio Django), e a página seguinte é
    sempre a mesma, exista ou não a conta.
    """

    def send_mail(self, subject_template_name, email_template_name, context, from_email,
                  to_email, html_email_template_name=None):  # fmt: skip
        if not services.pode_enviar_email(to_email):
            return
        link = services.link_absoluto("contas:redefinir_senha", context["uid"], context["token"])
        services.enviar_email(
            to_email,
            "Nova senha no site do Habonim Dror Brasil",
            "contas/emails/redefinir_senha.txt",
            {"user": context["user"], "link": link},
        )
