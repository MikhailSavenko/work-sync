from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class StatusTask(models.TextChoices):
        OPEN = "OP", _("Открыто")
        AT_WORK = "AW", _("В работе")
        DONE = "DN", _("Выполнено")

    title = models.CharField(max_length=255, verbose_name="Наименование задачи")
    description = models.TextField(verbose_name="Описание задачи")
    deadline = models.DateTimeField(verbose_name="Крайний срок")
    status = models.CharField(max_length=2, choices=StatusTask, default=StatusTask.OPEN, verbose_name="Статус задачи")
    executor = models.ForeignKey("Worker", verbose_name="Исполнитель", on_delete=models.SET_NULL, null=True, blank=True, related_name="executed_tasks")
    creator = models.ForeignKey("Worker", verbose_name="Создатель", on_delete=models.PROTECT, related_name="created_tasks")
    created_at = models.DateTimeField(verbose_name="Даты и время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Даты и время обновления", auto_now=True)
