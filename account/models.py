from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Worker(models.Model):
    class Role(models.TextChoices):
        NORMAL = "NM", _("Обычный пользователь")
        MANAGER = "MG", _("Менеджер")
        ADMIN_TEAM = "AT", _("Админ команды")

    user = models.OneToOneField("User", related_name="worker", on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Role, default=Role.NORMAL)
    team = models.ForeignKey("Team", related_name="workers", on_delete=models.SET_NULL, null=True, blank=True)



