from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from datetime import datetime, time
import calendar

from account.serializers import TeamCreateUpdateSerializer, WorkerGetSerializer, TeamGetSerializer
from account.models import Team, Worker

from event.models import Meeting
from task.models import Task
from event.serializers import MeetingGetSerializer
from task.serializers import GetTaskSerializer

from account.services.calendar import get_calendar_events



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

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end, request=request)

        return Response(data={
            "date": parse_date,
            **calendar_events
            })

    @action(detail=False, methods=["get"], url_path="calendar/month/(?P<date>\\d{4}-\\d{2})")
    def calendar_month(self, request, date):
        """
        Эндпоиинт просмотра событий сотрудника за месяц 
        date - обязательный параметр пути YYYY-MM
        """
        worker = request.user.worker
        parse_date = datetime.strptime(date, "%Y-%m").date()
        
        last_day_month = calendar.monthrange(parse_date.year, parse_date.month)[1]
        end_date = parse_date.replace(day=last_day_month)

        start = datetime.combine(parse_date, time.min)
        end = datetime.combine(end_date, time.max)

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end, request=request)

        return Response(data={
            "date": parse_date,
            **calendar_events
            })
    