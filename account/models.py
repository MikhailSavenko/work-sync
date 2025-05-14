from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Worker(models.Model):
    """
    Модель Worker, представляющая сотрудника компании.

    Атрибуты:
        user (OneToOneField): Связь с моделью User.
        role (CharField): Роль сотрудника в команде (обычный пользователь, менеджер, админ).
        team (ForeignKey): Связь с моделью Team; может быть None, если сотрудник не состоит в команде.
    """
    class Role(models.TextChoices):
        NORMAL = "NM", _("Обычный пользователь")
        MANAGER = "MG", _("Менеджер")
        ADMIN_TEAM = "AT", _("Админ команды")

    user = models.OneToOneField("User", related_name="worker", on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Role, default=Role.NORMAL)
    team = models.ForeignKey("Team", related_name="workers", on_delete=models.SET_NULL, null=True, blank=True)


class Team(models.Model):
    """
    Модель Team, представляющая команду в системе.

    Атрибуты:
        title (CharField): Название команды.
        description (CharField): Описание команды.

    Связи:
        workers (Reverse relation): Список связанных объектов Worker, привязанных к данной команде.
    """
    title = models.CharField(max_length=255, verbose_name="Название команды")
    description = models.TextField(verbose_name="Описание команды")
