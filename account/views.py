from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Prefetch

from datetime import datetime

from account.exceptions import TeamConflictError
from account.serializers import TeamCreateUpdateSerializer, WorkerGetSerializer, TeamGetSerializer
from account.models import Team, Worker

from account.services.calendar import get_calendar_events
from account.services.team import get_worker_with_team
from task.models import Evaluation
from account.utils import get_day_bounds, get_month_bounds


class TeamViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "put", "delete", "options", "head")
    permission_classes = (IsAuthenticated,)
    queryset = Team.objects.prefetch_related(Prefetch("workers", queryset=Worker.objects.select_related("user")))

    serializer_class = {
        "update": TeamCreateUpdateSerializer,
        "create": TeamCreateUpdateSerializer,
        "list": TeamGetSerializer,
        "retrieve": TeamGetSerializer,
    }
    # будет доступен admin_team

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, TeamGetSerializer)

    def perform_create(self, serializer):
        current_worker = self.request.user.worker

        workers_added = serializer.validated_data.get("workers")
        self._check_team_conflict(workers_added)

        serializer.save(creator=current_worker)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        workers_added = serializer.validated_data.get("workers")
        self._check_team_conflict(workers_added)
        return super().perform_update(serializer)
    
    def _check_team_conflict(self, workers: list[Worker]):
        """Проверяет конфликты команд для списка сотрудников"""
        if not workers:
            return

        check_conflict_team = get_worker_with_team(workers)
        if check_conflict_team:
            emails = [worker.user.email for worker in check_conflict_team]
            raise TeamConflictError({
                "detail": f"Конфликт. Сотрудники {emails}, добавляемые в команду, уже состоят в других командах."
            })
        
class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkerGetSerializer
    queryset = Worker.objects.all()

    @action(detail=True, methods=["get"], url_path=r"evaluation/avg/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})")
    def average_evaluation(self, request, start_date=None, end_date=None, pk=None):
        """
        Средняя оценка сотрудника
        start_date - начальная дата YYYY-MM-DD
        end_date - конечная дата YYYY-MM-DD
        """
        current_worker = self.get_object()
        
        parce_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        parse_end = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        start, end = get_day_bounds((parce_start, parse_end))

        evaluations = Evaluation.objects.filter(to_worker=current_worker, created_at__range=(start, end))

        avg = evaluations.aggregate(Avg("score"))

        return Response(data={
            "start_date": parce_start,
            "end_date": parse_end,
            "average_score": avg.get("score__avg") if avg is not None else None,
            "evaluations_count": evaluations.count()
        })

    @action(detail=True, methods=["get"], url_path=r"calendar/day/(?P<date>\d{4}-\d{2}-\d{2})")
    def calendar_day(self, request, date=None, pk=None):
        """
        Эндпоиинт просмотра событий сотрудника за день 
        date - обязательный параметр пути YYYY-MM-DD
        """
        worker = self.get_object()

        parse_date = datetime.strptime(date, "%Y-%m-%d").date()

        start, end = get_day_bounds(date=parse_date)

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

        start, end = get_month_bounds(start_date=parse_date)

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end, request=request)

        return Response(data={
            "date": parse_date,
            **calendar_events
            })
    