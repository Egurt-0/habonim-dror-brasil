from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        # Login sem diferenciar maiúsculas: "Pessoa@Exemplo.com" e "pessoa@exemplo.com" são a mesma.
        return self.get(email__iexact=email)

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Superusuário precisa de is_staff=True e is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Usuário do site. Login por e-mail; não há username."""

    username = None
    email = models.EmailField("e-mail", unique=True)
    # LGPD: quando a pessoa aceitou a política e declarou ter 18 anos ou mais (cadastro).
    aceitou_privacidade_em = models.DateTimeField(
        "aceitou a política de privacidade em", null=True, blank=True, editable=False
    )
    declarou_maioridade_em = models.DateTimeField(
        "declarou ter 18 anos ou mais em", null=True, blank=True, editable=False
    )
    snifim = models.ManyToManyField(
        "snifim.Snif",
        verbose_name="snifim que edita",
        related_name="editores",
        blank=True,
        help_text=(
            "Para contas do grupo editor_snif: os snifim que esta pessoa pode editar no painel."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        constraints = [models.UniqueConstraint(Lower("email"), name="email_unico_sem_maiusculas")]

    def __str__(self):
        return self.get_full_name() or self.email
