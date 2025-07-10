from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.variables import (
    CURRENT_TASK_ALREADY_HAS_SCORE,
    CURRENT_TASK_HASNT_EXECUTOR,
    CURRENT_TASK_WILL_BE_DONE_STATUS,
)
from task.doc.schemas import CommentAutoSchema, EvaluationAutoSchema, TaskAutoSchema
from task.exeptions import EvaluationConflictError, TaskConflictError
from task.models import Comment, Evaluation, Task
from task.permissions import IsCreatorAdminManager, IsCreatorAdminManagerOrReadOnly, IsCreatorOrReadOnly
from task.serializers import (
    CreateCommentSerializer,
    CreateEvaluation,
    GetCommentSerializer,
    GetTaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    UpdateCommentSerializer,
    UpdateEvaluation,
)
from task.utils import is_int_or_valid_error


class TaskViewSet(viewsets.ModelViewSet):
    """
    API для управления задачами.

    Предоставляет полный набор операций CRUD (Create, Retrieve, Update, Delete)
    для объектов задач. Доступ к задачам контролируется разрешениями на основе
    роли пользователя (создатель, администратор, менеджер) и его отношения к задаче.

    **Разрешенные HTTP-методы:**
    - GET: Получение списка всех задач или деталей конкретной задачи.
    - POST: Создание новой задачи.
    - PUT: Полное обновление существующей задачи.
    - PATCH: Частичное обновление существующей задачи.
    - DELETE: Удаление задачи.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """

    queryset = Task.objects.all()
    permission_classes = [IsCreatorAdminManagerOrReadOnly]
    swagger_schema = TaskAutoSchema
    serializer_class = {
        "list": GetTaskSerializer,
        "retrieve": GetTaskSerializer,
        "me": GetTaskSerializer,
        "update": TaskUpdateSerializer,
        "partial_update": TaskUpdateSerializer,
        "create": TaskCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, GetTaskSerializer)

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Получает список задач, назначенных текущему аутентифицированному пользователю (Worker).

        Этот эндпоинт возвращает все задачи, где текущий пользователь указан как исполнитель.
        Пользователи могут просматривать только свои задачи.

        :param request: Объект запроса Django REST Framework.
        :return: Ответ `Response` с JSON-списком задач.
        """
        user_worker = request.user.worker

        tasks = Task.objects.filter(executor=user_worker)
        serializer = self.get_serializer(tasks, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Сохраняет новую задачу, автоматически назначая текущего аутентифицированного
        пользователя (Worker) её создателем.
        """
        serializer.save(creator=self.request.user.worker)

    def perform_update(self, serializer):
        """
        Выполняет обновление задачи, включая валидацию для оцененных и завершенных задач.

        Запрещает изменение исполнителя (`executor`) или статуса (`status`)
        для задач, которые уже были оценены и завершены.

        :param serializer: Сериализатор, содержащий валидированные данные для обновления задачи.
        :raises TaskConflictError: Если предпринята попытка изменить исполнителя или статус
                                   оцененной и завершенной задачи.
        """
        executor = serializer.validated_data.get("executor")
        status = serializer.validated_data.get("status")
        instance = self.get_object()

        if hasattr(instance, "evaluation"):
            if executor and executor != instance.executor:
                raise TaskConflictError(
                    detail={
                        "task_update_conflict": "Ошибка. Нельзя изменить исполнителя(executor) для оцененной и завершенной задачи."
                    }
                )
            if status and status != instance.status:
                raise TaskConflictError(
                    detail={
                        "task_update_conflict": "Ошибка. Нельзя изменить статус(status) для оцененной и завершенной задачи."
                    }
                )
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    API для управления комментариями к задачам.

    Этот ViewSet позволяет выполнять операции CRUD (Create, Retrieve, Update, Delete)
    над комментариями, которые всегда привязаны к конкретной задаче. Доступ
    к комментариям контролируется на основе того, является ли пользователь их создателем.

    **Разрешенные HTTP-методы:**
    - GET: Получение списка комментариев для задачи или деталей конкретного комментария.
    - POST: Создание нового комментария для задачи.
    - PATCH: Частичное обновление существующего комментария.
    - DELETE: Удаление комментария.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """

    http_method_names = ("get", "post", "patch", "delete", "options", "head")
    queryset = Comment.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
    swagger_schema = CommentAutoSchema
    serializer_class = {
        "list": GetCommentSerializer,
        "retrieve": GetCommentSerializer,
        "partial_update": UpdateCommentSerializer,
        "create": CreateCommentSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, GetCommentSerializer)

    def perform_create(self, serializer):
        """
        Создает новый комментарий, связывая его с конкретной задачей
        и текущим аутентифицированным пользователем (Worker) как создателем.

        ID задачи (`task_pk`) должен быть передан в параметрах URL.

        :param serializer: Сериализатор, содержащий валидированные данные для создания комментария.
        :raises ValidationError: Если `task_pk` в URL не является целым числом.
        :raises Http404: Если задача с указанным `task_pk` не найдена.
        """
        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)

        task = get_object_or_404(Task, pk=task_pk)

        serializer.save(creator=self.request.user.worker, task=task)

    def get_queryset(self):
        """
        Возвращает queryset комментариев, отфильтрованных по задаче.

        Этот метод гарантирует, что все операции (list, retrieve) внутри этого ViewSet'а
        выполняются только для комментариев, относящихся к конкретной задаче,
        ID которой (`task_pk`) передается в URL.

        :raises ValidationError: Если `task_pk` в URL не является целым числом.
        :raises Http404: Если задача с указанным `task_pk` не найдена.
        :return: Отфильтрованный QuerySet объектов `Comment`.
        """
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()

        queryset = super().get_queryset()

        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)
        get_object_or_404(Task, pk=task_pk)

        comments = queryset.filter(task=task_pk)
        return comments


class EvaluationViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    API для управления оценками выполнения задач (Evaluation).

    Этот ViewSet позволяет создавать, обновлять и удалять оценки,
    которые всегда привязаны к конкретной задаче. Оценки могут быть
    добавлены только для **завершенных** задач, у которых есть **исполнитель**.
    Доступ контролируется разрешениями для создателя оценки, администраторов и менеджеров.

    **Разрешенные HTTP-методы:**
    - POST: Создание новой оценки для задачи.
    - PATCH: Частичное обновление существующей оценки.
    - DELETE: Удаление оценки.
    - OPTIONS, HEAD: Стандартные методы для интроспекции API.
    """

    http_method_names = ("post", "patch", "delete", "options", "head")
    queryset = Evaluation.objects.all()
    permission_classes = [IsCreatorAdminManager]
    swagger_schema = EvaluationAutoSchema
    serializer_class = {"create": CreateEvaluation, "partial_update": UpdateEvaluation}

    def get_serializer_class(self):
        return self.serializer_class.get(self.action)

    def perform_create(self, serializer):
        """
        Создает новую оценку для задачи, связывая её с задачей, её исполнителем
        и текущим аутентифицированным пользователем как автором оценки.

        Перед созданием оценки выполняется ряд проверок:
        1. Проверяется, что задача с `task_pk` существует.
        2. Проверяется, что у задачи еще нет оценки.
        3. Проверяется, что у задачи назначен исполнитель.
        4. Проверяется, что статус задачи установлен как "Выполнено" (DONE).

        :param serializer: Сериализатор, содержащий валидированные данные для создания оценки.
        :raises ValidationError: Если `task_pk` в URL не является целым числом.
        :raises Http404: Если задача с указанным `task_pk` не найдена.
        :raises EvaluationConflictError: Если задача уже имеет оценку, у неё нет исполнителя,
                                        или её статус не "Выполнено".
        """
        from_worker = self.request.user.worker

        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)

        task = get_object_or_404(Task, pk=task_pk)

        if hasattr(task, "evaluation"):
            raise EvaluationConflictError({"evaluation_create_conflict": CURRENT_TASK_ALREADY_HAS_SCORE})
        elif not task.executor:
            raise EvaluationConflictError({"evaluation_create_conflict": CURRENT_TASK_HASNT_EXECUTOR})
        elif task.status != Task.StatusTask.DONE:
            raise EvaluationConflictError({"evaluation_create_conflict": CURRENT_TASK_WILL_BE_DONE_STATUS})
        serializer.save(to_worker=task.executor, from_worker=from_worker, task=task)

    def get_queryset(self):
        """
        Возвращает queryset оценок, отфильтрованных по задаче.

        Этот метод обеспечивает, что операции по получению, обновлению и удалению
        оценок выполняются только для оценок, относящихся к конкретной задаче,
        ID которой (`task_pk`) передается в URL.

        :raises ValidationError: Если `task_pk` в URL не является целым числом.
        :raises Http404: Если задача с указанным `task_pk` не найдена.
        :return: Отфильтрованный QuerySet объектов `Evaluation`.
        """
        if getattr(self, "swagger_fake_view", False):
            return Evaluation.objects.none()

        queryset = super().get_queryset()

        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)
        get_object_or_404(Task, pk=task_pk)

        evaluation = queryset.filter(task=task_pk)
        return evaluation
