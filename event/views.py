from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from event.models import Meeting
from event.doc.schemas import MeetingAutoSchema
from event.serializers import MeetingGetSerializer, MeetingCreateUpdateSerializer
from event.permissions import IsOwnerOrReadOnly


class MeetingViewSet(viewsets.ModelViewSet):
    """
    API для управления встречами.

    Предоставляет полный набор операций CRUD (Create, Retrieve, Update, Delete)
    для объектов встреч. Пользователи могут управлять только теми встречами,
    в которых они являются создателем или участником с любой ролью(согласно IsOwnerOrReadOnly).

    **Разрешенные HTTP-методы:**
    - GET: Получение списка всех встреч или деталей конкретной встречи.
    - POST: Создание новой встречи.
    - PUT: Полное обновление существующей встречи.
    - DELETE: Удаление встречи.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """
    http_method_names = ("get", "post", "put", "delete", "options", "head")
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Meeting.objects.all()
    serializer_class = {
        "list": MeetingGetSerializer,
        "retrieve": MeetingGetSerializer,
        "me": MeetingGetSerializer,
        "update": MeetingCreateUpdateSerializer,
        "create": MeetingCreateUpdateSerializer,
    }
    swagger_schema = MeetingAutoSchema

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, MeetingGetSerializer)
    
    def perform_create(self, serializer):
        current_user = self.request.user.worker
        serializer.save(creator=current_user)
    
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Получает список встреч, связанных с текущим аутентифицированным пользователем.

        Этот эндпоинт позволяет фильтровать встречи по их статусу: **предстоящие** или **завершенные**.

        **Параметры запроса (Query Parameters):**
        * `done` (тип: `string`, по умолчанию: `"0"`) - Флаг для фильтрации встреч.
            * Если `"0"` (или параметр отсутствует), возвращаются только **предстоящие встречи** (где время встречи в будущем).
            * Если `"1"`, возвращаются все встречи в том числе и **завершенные встречи** (где время встречи в прошлом).

        :param request: Объект запроса Django REST Framework.
        :return: Ответ `Response` с JSON-списком встреч.
        :raises status.HTTP_400_BAD_REQUEST: Если параметр `done` имеет некорректное значение (отличное от "0" или "1").
        """
        user_worker = request.user.worker
        done_param = request.query_params.get("done", "0")
        
        if done_param not in ("0", "1"):
            return Response(
                {"detail": "Парамтер 'done' может быть 0 или 1"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        queryset = super().get_queryset()

        if done_param == "1":
            meetings = queryset.filter(workers=user_worker)
        elif done_param == "0":
            now = timezone.now()
            meetings = queryset.filter(workers=user_worker, datetime__gt=now)
        
        serializer = self.get_serializer_class()
        serializer = serializer(meetings, many=True)

        return Response(serializer.data)