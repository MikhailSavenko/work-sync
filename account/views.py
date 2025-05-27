from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from datetime import datetime, time
import calendar
from django.utils import timezone

from account.serializers import TeamCreateUpdateSerializer, WorkerGetSerializer, TeamGetSerializer
from account.models import Team, Worker

from account.services.calendar import get_calendar_events
from task.models import Evaluation


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

    @action(detail=False, methods=["get"], url_path=r"evaluation/avg/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})")
    def average_evaluation(self, request, start_date, end_date):
        """Средняя оценка сотрудника"""
        current_worker = request.user.worker
        
        parce_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        parse_end = datetime.strptime(end_date, "%Y-%m-%d").date()

        start = datetime.combine(parce_start, time.min)
        end = datetime.combine(parse_end, time.max)

        evaluations = Evaluation.objects.filter(to_worker=current_worker, created_at__range=(start, end))

        avg = evaluations.aggregate(Avg("score"))

        return Response(data={
            "worker_id": current_worker.id,
            "start_date": parce_start,
            "end_date": parse_end,
            "average_score": avg.get("score__avg") if avg is not None else None,
            "evaluations_count": evaluations.count()
        })

    @action(detail=False, methods=["get"], url_path=r"calendar/day/(?P<date>\d{4}-\d{2}-\d{2})")
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

    @action(detail=True, methods=["get"], url_path=r"calendar/month/(?P<date>\d{4}-\d{2})")
    def calendar_month(self, request, date=None, pk=None):
        """
        Эндпоиинт просмотра событий сотрудника за месяц 
        date - обязательный параметр пути YYYY-MM
        """
        worker = self.get_object()
        parse_date = datetime.strptime(date, "%Y-%m").date()
        
        last_day_month = calendar.monthrange(parse_date.year, parse_date.month)[1]
        end_date = parse_date.replace(day=last_day_month)

        start = timezone.make_aware(datetime.combine(parse_date, time.min))
        end = timezone.make_aware(datetime.combine(end_date, time.max))

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end, request=request)

        return Response(data={
            "date": parse_date,
            **calendar_events
            })
    