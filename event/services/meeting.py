from account.models import Worker
from rest_framework import serializers
from datetime import datetime
from event.models import Meeting


def validate_workers_and_include_creator(creator: Worker, workers: list[Worker]) -> list[Worker]:
    """
    Проверяет участников встречи, добавляет создателя и гарантирует минимум двух уникальных участников.

    :param creator: Создатель встречи.
    :type creator: account.models.Worker
    :param workers: Список приглашенных участников.
    :type workers: list[account.models.Worker]
    :raises serializers.ValidationError: Если список участников пуст или менее двух уникальных участников.
    :returns: Список уникальных участников, включая создателя.
    :rtype: list[account.models.Worker]
    """
    if not workers:
        raise serializers.ValidationError("Укажите хотя бы одного сотрудника для встречи.")

    workers = list(workers)

    if creator not in workers:
        workers.append(creator)

    if len(set(workers)) < 2:
        raise serializers.ValidationError("Встреча должна включать минимум двух участников.")
    
    return workers


def check_if_datetime_is_free(worker: Worker, check_date: datetime) -> bool:
    """
    Проверяет, свободно ли указанное время для сотрудника, сравнивая с уже назначенными встречами.

    :param worker: Сотрудник, для которого проверяется доступность времени.
    :type worker: account.models.Worker
    :param check_date: Дата и время для проверки.
    :type check_date: datetime.datetime
    :returns: True, если время свободно, False в противном случае.
    :rtype: bool
    """
    meetings_datetimes = Meeting.objects.filter(workers=worker).values_list("datetime", flat=True)
      
    for meeting_datetime in meetings_datetimes:
        if meeting_datetime == check_date:
            return False
    
    return True