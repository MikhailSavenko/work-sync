from django.db import models
from account.models import Worker


class Meeting(models.Model):
    """
    Модель встречи.

    Поля:
    - datetime: дата и время проведения встречи.
    - creator: сотрудник-инициатор встречи.
    - workers: сотрудники, приглашённые на встречу (через промежуточную модель MeetingWorker).
    """
    datetime = models.DateTimeField(verbose_name="Дата и время встречи")
    creator = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name="Инициатор встречи", related_name="created_meetings")
    workers = models.ManyToManyField(Worker, through="MeetingWorker", related_name="meetings", verbose_name="Сотрудники приглашенные на встречу")


class MeetingWorker(models.Model):
    """
    Промежуточная модель связи между встречей и сотрудниками.

    Поля:
    - worker: сотрудник, приглашённый на встречу.
    - meeting: встреча, на которую приглашён сотрудник.
    """
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)