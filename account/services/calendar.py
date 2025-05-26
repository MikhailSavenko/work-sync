from event.models import Meeting
from task.models import Task
from event.serializers import MeetingGetSerializer
from task.serializers import GetTaskSerializer
from account.models import Worker

from tabulate import tabulate


def get_calendar_events(worker: Worker, start_date, end_date, request):
    meetings = Meeting.objects.filter(workers=worker, datetime__range=(start_date, end_date))
    tasks = Task.objects.filter(executor=worker, deadline__range=(start_date, end_date))

    meeting_serializer_data = MeetingGetSerializer(meetings, many=True)
    tasks_serializer_data = GetTaskSerializer(tasks, many=True, context={"request": request})
    
    table = format_calendar_text_table(meetings, tasks)

    return {
        "meetings": meeting_serializer_data.data,
        "tasks": tasks_serializer_data.data,
        "table": table.splitlines()
    }


def format_calendar_text_table(meetings, tasks):
    table = []

    for meeting in meetings:
        table.append(["Встреча", meeting.datetime.strftime("%d.%m.%Y %H:%M"), meeting.description])

    for task in tasks:
        table.append(["Задача", task.deadline.strftime("%d.%m.%Y %H:%M"), task.title])
    print("В ТАБУЛЭЙТ")

    return tabulate(table, headers=["Тип", "Дата и время", "Описание"], tablefmt="grid")