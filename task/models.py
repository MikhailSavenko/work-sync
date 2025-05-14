from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import Worker


class Task(models.Model):
    """
    Модель задачи.

    Атрибуты:
        title (str): Наименование задачи.
        description (str): Подробное описание задачи.
        deadline (datetime): Крайний срок выполнения.
        status (str): Текущий статус задачи (Открыто, В работе, Выполнено).
        executor (Worker | None): Исполнитель задачи. Может быть не назначен.
        creator (Worker): Создатель задачи. Удаление запрещено.
        created_at (datetime): Дата и время создания задачи (автоматически устанавливается).
        updated_at (datetime): Дата и время последнего обновления задачи (обновляется автоматически).

    Связи:
        - executor.executed_tasks — список задач, в которых работник является исполнителем.
        - creator.created_tasks — список задач, созданных работником.
    """
    class StatusTask(models.TextChoices):
        OPEN = "OP", _("Открыто")
        AT_WORK = "AW", _("В работе")
        DONE = "DN", _("Выполнено")

    title = models.CharField(max_length=255, verbose_name="Наименование задачи")
    description = models.TextField(verbose_name="Описание задачи")
    deadline = models.DateTimeField(verbose_name="Крайний срок")
    status = models.CharField(max_length=2, choices=StatusTask, default=StatusTask.OPEN, verbose_name="Статус задачи")
    executor = models.ForeignKey(Worker, verbose_name="Исполнитель", on_delete=models.SET_NULL, null=True, blank=True, related_name="executed_tasks")
    creator = models.ForeignKey(Worker, verbose_name="Создатель", on_delete=models.PROTECT, related_name="created_tasks")
    created_at = models.DateTimeField(verbose_name="Даты и время создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Даты и время обновления", auto_now=True)


class Evaluation(models.Model):
    """
    Модель оценки выполнения задачи.

    Поля:
    - score: числовая оценка выполнения (от 1 до 5).
    - task: задача, которая оценивается (одна задача — одна оценка).
    - to_worker: сотрудник, которого оценивают (может быть None при удалении).
    - from_worker: сотрудник, который выставил оценку (может быть None при удалении).
    """
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка выполния задачи", 
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    task = models.OneToOneField(Task, verbose_name="Оцениваемая задача", on_delete=models.CASCADE)
    to_worker = models.ForeignKey(Worker, verbose_name="Оценен", on_delete=models.SET_NULL, null=True, blank=True, related_name="received_evaluations")
    from_worker = models.ForeignKey(Worker, verbose_name="Оценил", on_delete=models.SET_NULL, null=True, blank=True, related_name="given_evaluations")