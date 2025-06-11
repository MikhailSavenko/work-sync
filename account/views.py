from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView as TokenObtainPairViewBase, TokenBlacklistView as TokenBlacklistViewBase, TokenRefreshView as TokenRefreshViewBase

from django.db.models import Prefetch

from datetime import datetime

from account.doc.schemas import TeamAutoSchema, WorkerAutoSchema, TokenObtainAutoSchema, TokenBlacklistAutoSchema, TokenRefreshAutoSchema
from account.exceptions import TeamConflictError
from account.serializers import TeamCreateUpdateSerializer, WorkerEvaluationResponseSerializer, WorkerCalendarResponseSerializer, WorkerGetSerializer, TeamGetSerializer, WorkerUpdateSerializer
from account.models import Team, Worker

from account.services.worker import get_calendar_events, get_evaluations_avg
from account.services.team import get_worker_with_team
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
    swagger_schema = TeamAutoSchema
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
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin):
    http_method_names = ("get", "patch", "options", "head")
    # permission_classes = (IsAuthenticated,)
    serializer_class = WorkerGetSerializer
    queryset = Worker.objects.all()
    serializer_class = {
        "list": WorkerGetSerializer,
        "retrieve": WorkerGetSerializer,
        "partial_update": WorkerUpdateSerializer,
        "calendar_day": WorkerCalendarResponseSerializer,
        "calendar_month": WorkerCalendarResponseSerializer,
        "average_evaluation": WorkerEvaluationResponseSerializer
    }
    swagger_schema = WorkerAutoSchema
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, WorkerGetSerializer)
    
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

        evaluation_avg = get_evaluations_avg(worker=current_worker, start=start, end=end)

        data = {"start_date": parce_start, "end_date": parse_end, **evaluation_avg}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data)

        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path=r"calendar/day/(?P<date>\d{4}-\d{2}-\d{2})")
    def calendar_day(self, request, date=None, pk=None):
        """
        Эндпоиинт просмотра событий сотрудника за день 
        date - обязательный параметр пути YYYY-MM-DD
        """
        worker = self.get_object()

        parse_date = datetime.strptime(date, "%Y-%m-%d").date()

        start, end = get_day_bounds(date=parse_date)

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end)
        
        data = {"date": parse_date, **calendar_events}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path=r"calendar/month/(?P<date>\d{4}-\d{2})")
    def calendar_month(self, request, date=None, pk=None):
        """
        Эндпоиинт просмотра событий сотрудника за месяц 
        date - обязательный параметр пути YYYY-MM
        """
        worker = self.get_object()
        parse_date = datetime.strptime(date, "%Y-%m").date()

        start, end = get_month_bounds(start_date=parse_date)

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end)

        data = {"date": parse_date, **calendar_events}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data, context={"request": request})
        return Response(serializer.data)


class TokenObtainPairView(TokenObtainPairViewBase):
    swagger_schema = TokenObtainAutoSchema


class TokenBlacklistView(TokenBlacklistViewBase):
    swagger_schema = TokenBlacklistAutoSchema


class TokenRefreshView(TokenRefreshViewBase):
    swagger_schema = TokenRefreshAutoSchema