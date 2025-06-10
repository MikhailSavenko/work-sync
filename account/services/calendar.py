from event.models import Meeting
from task.models import Task
from account.models import Worker

from tabulate import tabulate


def get_calendar_events(worker: Worker, start_date, end_date):
    meetings = Meeting.objects.prefetch_related("workers").filter(workers=worker, datetime__range=(start_date, end_date))
    tasks = Task.objects.select_related("executor").filter(executor=worker, deadline__range=(start_date, end_date))
    
    table = format_calendar_text_table(meetings, tasks)

    return {
        "meetings": meetings,
        "tasks": tasks,
        "table": table.splitlines()
    }


def format_calendar_text_table(meetings, tasks):
    table = []

    for meeting in meetings:
        table.append(["Встреча", meeting.datetime.strftime("%d.%m.%Y %H:%M"), meeting.description, ", ".join(worker.user.email for worker in meeting.workers.all())])

    for task in tasks:
        table.append(["Задача", task.deadline.strftime("%d.%m.%Y %H:%M"), task.title, task.executor.user.email])

    return tabulate(table, headers=["Тип", "Дата и время", "Описание", "Участники"], tablefmt="grid")