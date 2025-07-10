import logging
from datetime import datetime

from django.db.models import Prefetch
from djoser.views import UserViewSet as UserViewSetBase
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView as TokenBlacklistViewBase
from rest_framework_simplejwt.views import TokenObtainPairView as TokenObtainPairViewBase
from rest_framework_simplejwt.views import TokenRefreshView as TokenRefreshViewBase
from rest_framework_simplejwt.views import TokenVerifyView as TokenVerifyViewBase

from account.doc.schemas import (
    TeamAutoSchema,
    TokenBlacklistAutoSchema,
    TokenObtainAutoSchema,
    TokenRefreshAutoSchema,
    TokenVerifyAutoSchema,
    UserAutoSchema,
    WorkerAutoSchema,
)
from account.exceptions import TeamConflictError, ValidationDateError
from account.models import Team, Worker
from account.permissions import IsAdminTeamOrReadOnly, IsAdminTeamOwnerOrReadOnly
from account.serializers import (
    TeamCreateUpdateSerializer,
    TeamGetSerializer,
    WorkerCalendarResponseSerializer,
    WorkerEvaluationResponseSerializer,
    WorkerGetSerializer,
    WorkerUpdateSerializer,
)
from account.services.team import get_worker_with_team, is_your_team
from account.services.worker import get_calendar_events, get_evaluations_avg
from account.utils import get_day_bounds, get_month_bounds

logger = logging.getLogger(__name__)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API для управления командами.

    Этот ViewSet предоставляет полный набор операций CRUD (Create, Retrieve, Update, Delete)
    для объектов команд. Доступ к командам контролируется разрешениями на основе
    роли пользователя (администратор, владелец команды).

    **Разрешенные HTTP-методы:**
    - GET: Получение списка всех команд или деталей конкретной команды.
    - POST: Создание новой команды.
    - PUT: Полное обновление существующей команды.
    - DELETE: Удаление команды.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """

    http_method_names = ("get", "post", "put", "delete", "options", "head")
    permission_classes = [IsAdminTeamOwnerOrReadOnly]
    queryset = Team.objects.prefetch_related(Prefetch("workers", queryset=Worker.objects.select_related("user")))
    serializer_class = {
        "update": TeamCreateUpdateSerializer,
        "create": TeamCreateUpdateSerializer,
        "list": TeamGetSerializer,
        "retrieve": TeamGetSerializer,
    }
    swagger_schema = TeamAutoSchema

    def get_serializer_class(self):
        serializer = self.serializer_class.get(self.action)

        if serializer is None:
            logger.warning(
                f"Не найден сериализатор для действия '{self.action}' в {self.__class__.__name__}. "
                f"Используется TeamGetSerializer как запасной."
            )
            return TeamGetSerializer

        return serializer

    def perform_create(self, serializer):
        """
        Создает новую команду, автоматически назначая текущего аутентифицированного
        пользователя (Worker) её создателем.

        Перед сохранением команды выполняется проверка на предмет того,
        не состоят ли добавляемые сотрудники уже в других командах.

        :param serializer: Сериализатор, содержащий валидированные данные для создания команды.
        :raises TeamConflictError: Если один или несколько добавляемых сотрудников уже состоят в других командах.
        """
        current_worker = self.request.user.worker

        workers_added = serializer.validated_data.get("workers")
        self._check_team_conflict(workers_added)

        serializer.save(creator=current_worker)

    def perform_update(self, serializer):
        """
        Обновляет существующую команду.

        Перед сохранением обновлений выполняется проверка на предмет того,
        не состоят ли добавляемые/изменяемые сотрудники уже в других командах.

        :param serializer: Сериализатор, содержащий валидированные данные для обновления команды.
        :raises TeamConflictError: Если один или несколько добавляемых/изменяемых сотрудников
                                   уже состоят в других командах, отличных от текущей.
        """
        team_pk = self.kwargs.get("pk")

        workers_added = serializer.validated_data.get("workers")
        self._check_team_conflict(workers_added, team_pk=team_pk)
        super().perform_update(serializer)

    def _check_team_conflict(self, workers: list[Worker], team_pk: int = None):
        """
        Проверяет потенциальные конфликты, если сотрудники уже состоят в других командах.

        Этот вспомогательный метод итерируется по списку предполагаемых сотрудников для добавления
        и проверяет, не привязаны ли они уже к какой-либо команде.

        :param workers: Список объектов `Worker`, которые должны быть добавлены или обновлены в команде.
        :param team_pk: (Опционально) Первичный ключ текущей команды. Если предоставленый
                        сотрудник может быть уже в этой *же* команде без конфликта.
        :raises TeamConflictError: Если обнаружен хотя бы один сотрудник, который
                                   уже состоит в другой команде.
        """
        if not workers:
            return

        conflicting_emails = []

        workers_already_in_team = get_worker_with_team(workers)
        for worker in workers_already_in_team:
            if team_pk is not None:
                if is_your_team(team_pk=team_pk, worker=worker):
                    continue
                else:
                    conflicting_emails.append(worker.user.email)
            else:
                conflicting_emails.append(worker.user.email)
        if conflicting_emails:
            raise TeamConflictError(
                {
                    "detail": f"Конфликт. Сотрудники {conflicting_emails}, добавляемые в команду, уже состоят в других командах."
                }
            )


class WorkerViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    """
    API для управления данными о сотрудниках.

    Предоставляет операции для получения списка сотрудников, деталей конкретного сотрудника,
    а также частичного обновления информации о сотруднике. Включает специализированные
    эндпоинты для просмотра календаря и средней оценки производительности.

    **Разрешенные HTTP-методы:**
    - GET: Получение списка всех сотрудников или деталей конкретного сотрудника.
    - PATCH: Частичное обновление данных сотрудника.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """

    http_method_names = ("get", "patch", "options", "head")
    permission_classes = [IsAdminTeamOrReadOnly]
    queryset = Worker.objects.all()
    serializer_class = {
        "list": WorkerGetSerializer,
        "retrieve": WorkerGetSerializer,
        "partial_update": WorkerUpdateSerializer,
        "calendar_day": WorkerCalendarResponseSerializer,
        "calendar_month": WorkerCalendarResponseSerializer,
        "average_evaluation": WorkerEvaluationResponseSerializer,
    }
    swagger_schema = WorkerAutoSchema

    def get_serializer_class(self):
        serializer = self.serializer_class.get(self.action)

        if serializer is None:
            logger.warning(
                f"Не найден сериализатор для действия '{self.action}' в {self.__class__.__name__}. "
                f"Используется WorkerGetSerializer как запасной."
            )
            return WorkerGetSerializer

        return serializer

    @action(
        detail=True,
        methods=["get"],
        url_path=r"evaluation/avg/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})",
    )
    def average_evaluation(self, request, start_date=None, end_date=None, pk=None):
        """
        Рассчитывает среднюю оценку производительности сотрудника за указанный период.

        Эта функция агрегирует все оценки, связанные с данным сотрудником,
        и возвращает их среднее значение. Период задается начальной и конечной датами.

        :param start_date: Начальная дата периода в формате YYYY-MM-DD.
        :param end_date: Конечная дата периода в формате YYYY-MM-DD.
        :param pk: ID сотрудника, для которого рассчитывается оценка.
        :return: JSON-ответ, содержащий среднюю оценку, количество задач, и даты запроса.
        :raises ValueError: Если формат даты не соответствует YYYY-MM-DD.
        """
        current_worker = self.get_object()
        try:
            parce_start = datetime.strptime(start_date, "%Y-%m-%d").date()
            parse_end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValidationDateError(detail=f"{e}")

        start, end = get_day_bounds((parce_start, parse_end))

        evaluation_avg = get_evaluations_avg(worker=current_worker, start=start, end=end)

        data = {"start_date": parce_start, "end_date": parse_end, **evaluation_avg}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data)

        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path=r"calendar/day/(?P<date>\d{4}-\d{2}-\d{2})")
    def calendar_day(self, request, date=None, pk=None):
        """
        Возвращает календарные события сотрудника за указанный день.

        Данный эндпоинт предоставляет консолидированный обзор расписания сотрудника за заданную дату,
        включая:
        - Все запланированные **события**.
        - **Задачи**, срок выполнения которых истекает в этот день.
        - **Встречи**, запланированные на этот день.

        Ответ содержит исчерпывающий ежедневный обзор всех обязательств сотрудника.

        :param date: Обязательный параметр пути в формате YYYY-MM-DD, представляющий день для получения событий.
        :param pk: ID сотрудника, чей календарь просматривается.
        :return: JSON-ответ, содержащий указанную дату и словарь со связанными календарными событиями, задачами и встречами, а также таблицу списком строк.
        :raises ValidationError: Если параметр пути 'date' не соответствует ожидаемому формату YYYY-MM-DD.
        """
        worker = self.get_object()

        try:
            parse_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValidationDateError(detail=f"{e}")

        start, end = get_day_bounds(date=parse_date)

        calendar_events = get_calendar_events(worker=worker, start_date=start, end_date=end)

        data = {"date": parse_date, **calendar_events}
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path=r"calendar/month/(?P<date>\d{4}-\d{2})")
    def calendar_month(self, request, date=None, pk=None):
        """
        Возвращает календарные события сотрудника за указанный месяц.

        Данный эндпоинт предоставляет агрегированный обзор расписания сотрудника за заданный месяц,
        включая:
        - Все запланированные **события**.
        - **Задачи**, срок выполнения которых истекает в течение месяца.
        - **Встречи**, запланированные на этот месяц.
        Ответ содержит полный ежемесячный обзор всех событий сотрудника.

        :param date: Обязательный параметр пути в формате YYYY-MM, представляющий месяц для получения событий.
        :param pk: ID сотрудника, чей календарь просматривается.
        :return: JSON-ответ, содержащий указанный месяц и словарь со связанными календарными событиями, задачами и встречами.
        :raises ValueError: Если параметр пути 'date' не соответствует ожидаемому формату YYYY-MM.
        """
        worker = self.get_object()

        try:
            parse_date = datetime.strptime(date, "%Y-%m").date()
        except ValueError as e:
            raise ValidationDateError(detail=f"{e}")

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


class TokenVerifyView(TokenVerifyViewBase):
    swagger_schema = TokenVerifyAutoSchema


class UserViewSet(UserViewSetBase):
    swagger_schema = UserAutoSchema
