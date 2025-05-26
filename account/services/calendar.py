from event.models import Meeting
from task.models import Task
from event.serializers import MeetingGetSerializer
from task.serializers import GetTaskSerializer
from account.models import Worker


def get_calendar_events(worker: Worker, start_date, end_date, request):
    meetings = Meeting.objects.filter(workers=worker, datetime__range=(start_date, end_date))
    tasks = Task.objects.filter(executor=worker, deadline__range=(start_date, end_date))

    meeting_serializer_data = MeetingGetSerializer(meetings, many=True)
    tasks_serializer_data = GetTaskSerializer(tasks, many=True, context={"request": request})

    return {
        "meetings": meeting_serializer_data.data,
        "tasks": tasks_serializer_data.data
    }