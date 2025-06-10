from event.models import Meeting
from task.models import Evaluation, Task
from account.models import Worker

from django.db.models import Avg

from tabulate import tabulate
from datetime import datetime
from typing import Dict, List, Union


def get_evaluations_avg(worker: Worker, start: datetime, end: datetime) -> Dict[str, Union[float, int, None]]:
    """
    Рассчитывает среднюю оценку и количество оценок для сотрудника за указанный период.

    Период определяется включительно (start <= created_at <= end).
    Функция работает с timezone-aware объектами datetime.datetime.

    :param worker: Объект сотрудника (Worker), для которого рассчитывается оценка.
    :type worker: Worker
    :param start: Начальная дата и время периода (включительно),
                  должно быть timezone-aware datetime.datetime объектом.
    :type start: datetime.datetime
    :param end: Конечная дата и время периода (включительно),
                должно быть timezone-aware datetime.datetime объектом.
    :type end: datetime.datetime
    :returns: Словарь с средней оценкой ('average_score') и количеством оценок ('evaluations_count').
              'average_score' может быть None, если нет оценок.
    :rtype: dict
    """
    
    evaluations = Evaluation.objects.filter(to_worker=worker, created_at__range=(start, end))
    avg = evaluations.aggregate(Avg("score"))
    print(start)
    data = {
        "average_score": avg.get("score__avg"),
        "evaluations_count": evaluations.count()
    }
    return data


def get_calendar_events(worker: Worker, start_date: datetime, end_date: datetime) -> Dict[str, Union[List['Meeting'], List['Task'], List[str]]]:
    """
    Получает события календаря (встречи и задачи) для конкретного сотрудника
    в заданном диапазоне дат и времени.

    Фильтрует встречи по полю 'datetime' и задачи по 'deadline',
    обеспечивая, что оба поля попадают в указанный диапазон
    (start_date <= событие <= end_date). Возвращает QuerySet'ы
    для встреч и задач, а также их текстовое представление в виде таблицы.

    :param worker: Объект сотрудника (`Worker`), для которого ищутся события.
    :type worker: Worker
    :param start_date: Начальная дата и время для фильтрации событий (включительно).
                       Должен быть timezone-aware `datetime.datetime` объектом.
    :type start_date: datetime.datetime
    :param end_date: Конечная дата и время для фильтрации событий (включительно).
                     Должен быть timezone-aware `datetime.datetime` объектом.
    :type end_date: datetime.datetime
    :returns: Словарь, содержащий QuerySet'ы встреч (`meetings`), задач (`tasks`)
              и список строк (`table`) с отформатированной текстовой таблицей событий.
    :rtype: dict
    """
    meetings = Meeting.objects.prefetch_related("workers").filter(workers=worker, datetime__range=(start_date, end_date))
    tasks = Task.objects.select_related("executor").filter(executor=worker, deadline__range=(start_date, end_date))
    
    table = format_calendar_text_table(meetings, tasks)

    return {
        "meetings": meetings,
        "tasks": tasks,
        "table": table.splitlines()
    }


def format_calendar_text_table(meetings: List[Meeting], tasks: List[Task]) -> str:
    """Форматирует списки встреч и задач в читаемую текстовую таблицу.

    Эта функция обрабатывает предоставленные QuerySet'ы или списки экземпляров моделей
    встреч и задач. Она извлекает ключевую информацию (дату, время, описание, участников/исполнителя)
    из каждого события и преобразует ее в строки таблицы. Конечная таблица
    генерируется с использованием библиотеки `tabulate` в формате сетки.

    :param meetings: Список или QuerySet экземпляров моделей `Meeting`.
                     Каждый объект `Meeting` должен иметь атрибуты `datetime` (datetime.datetime),
                     `description` (str) и связанное поле `workers` (ManyRelatedManager).
    :type meetings: list[Meeting]
    :param tasks: Список или QuerySet экземпляров моделей `Task`.
                  Каждый объект `Task` должен иметь атрибуты `deadline` (datetime.datetime),
                  `title` (str) и связанное поле `executor` (Worker).
    :type tasks: list[Task]
    :returns: Строка, представляющая отформатированную текстовую таблицу
              с заголовками "Тип", "Дата и время", "Описание", "Участники".
    :rtype: str
    """
    table = []

    for meeting in meetings:
        table.append(["Встреча", meeting.datetime.strftime("%d.%m.%Y %H:%M"), meeting.description, ", ".join(worker.user.email for worker in meeting.workers.all())])

    for task in tasks:
        table.append(["Задача", task.deadline.strftime("%d.%m.%Y %H:%M"), task.title, task.executor.user.email])

    return tabulate(table, headers=["Тип", "Дата и время", "Описание", "Участники"], tablefmt="grid")