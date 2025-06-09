from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from account.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Worker(models.Model):
    """
    Модель Worker, представляющая сотрудника компании.

    Атрибуты:
        user (OneToOneField): Связь с моделью User.
        role (CharField): Роль сотрудника в команде (обычный пользователь, менеджер, админ).
        team (ForeignKey): Связь с моделью Team; может быть None, если сотрудник не состоит в команде.

    Связи:
        executed_tasks (Reverse relation): Список задач(Task) пользователя-исполнителя
        created_tasks (Reverse relation): Список задач(Task) пользователя-создателя
        created_teams (Reverse relation): Список команд(Team) пользователя-создателя
        received_evaluations (Reverse relation): Полученные оценки(Evaluation)
        given_evaluations (Reverse relation): Поставленные оценки(Evaluation)
        comments (Reverse relation): Оставленные комментарии к задачам
        meetings (Reverse relation): Встречи сотрудника
        created_meetings (Reverse relation): Встречи организованные сотрудником
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
        creator: сотрудник, создавший команду.
        created_at: дата и время создания команды.
        updated_at: дата и время последнего изменения команды.

    Связи:
        workers (Reverse relation): Список связанных объектов Worker, привязанных к данной команде.
        
    """
    title = models.CharField(max_length=255, verbose_name="Название команды")
    description = models.TextField(verbose_name="Описание команды")

    creator = models.ForeignKey(Worker, verbose_name="Создатель", on_delete=models.PROTECT, related_name="created_teams")
    created_at = models.DateTimeField(verbose_name="Даты и время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Даты и время обновления", auto_now=True)