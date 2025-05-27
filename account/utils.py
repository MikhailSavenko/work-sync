from datetime import datetime, time
from django.utils import timezone
from typing import Union, Tuple
import calendar


def get_day_bounds(date: Union[Tuple[datetime], datetime]) -> Tuple[datetime, datetime]:
    """
    Возвращает временные границы (начало и конец дня или диапазона дней).
    
    - Если передан список из двух дат — считает их как start и end.
    - Если передана одна дата — возвращает границы этого дня.
    """
    if isinstance(date, tuple):
        if len(date) != 2:
            raise ValueError("Если передаем список, он должен содержать две даты!")
        start_date, end_date = date
    else:
        start_date = end_date = date

    start = timezone.make_aware(datetime.combine(start_date, time.min))
    end = timezone.make_aware(datetime.combine(end_date, time.max))

    return start, end


def get_month_bounds(start_date: datetime) -> Tuple[datetime, datetime]:
    """
    Возвращает временные границы месяца для переданной даты.

    Принимает дату (обычно — первый день месяца) и возвращает два timezone-aware объекта datetime:
    - начало месяца (00:00:00 первого дня),
    - конец месяца (23:59:59.999999 последнего дня).

    Использует вспомогательную функцию `get_day_bounds`.

    :param start_date: Дата, указывающая на нужный месяц.
    :return: Кортеж из двух datetime: (start, end)
    """
    last_day_month = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = start_date.replace(day=last_day_month)

    start, end = get_day_bounds((start_date, end_date))
    
    return start, end