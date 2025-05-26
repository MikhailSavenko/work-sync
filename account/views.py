from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from datetime import datetime, time


from account.serializers import TeamCreateUpdateSerializer, WorkerGetSerializer, TeamGetSerializer
from account.models import Team, Worker

from event.models import Meeting
from task.models import Task
from event.serializers import MeetingSerializer
from task.serializers import GetTaskSerializer

class TeamViewSet(viewsets.ModelViewSet):
    """Представление для Team"""
    queryset = Team.objects.select_related("user", "team").all()

    # будет доступен admin_team

    def get_serializer_class(self):
        if self.action == "update":
            self.serializer_class = TeamCreateUpdateSerializer
        elif self.action == "retrieve":
            self.serializer_class = TeamGetSerializer
        elif self.action == "list":
            self.serializer_class = TeamGetSerializer
        return self.serializer_class


class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkerGetSerializer
    queryset = Worker.objects.all()

    @action(detail=False, methods=["get"], url_path="calendar/day/(?P<date>\\d{4}-\\d{2}-\\d{2})")
    def calendar_day(self, request, date):
        """
        Эндпоиинт просмотра событий сотрудника за день 
        date - обязательный параметр пути YYYY-MM-DD
        """
        worker = request.user.worker

        parse_date = datetime.strptime(date, "%Y-%m-%d").date()
        start = datetime.combine(parse_date, time.min)
        end = datetime.combine(parse_date, time.max)

        meetings = Meeting.objects.filter(workers=worker, datetime__range=(start, end))
        tasks = Task.objects.filter(executor=worker, deadline__range=(start, end))

        meeting_serializer_data = MeetingSerializer(meetings, many=True)
        tasks_serializer_data = GetTaskSerializer(tasks, many=True, context={"request": request})

        return Response(data={
            "date": parse_date,
            "meetings": meeting_serializer_data.data,
            "tasks": tasks_serializer_data.data
            })

    