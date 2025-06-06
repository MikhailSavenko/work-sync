from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from task.doc.schemas import TaskAutoSchema, CommentAutoSchema
from task.models import Evaluation, Task, Comment
from task.serializers import TaskCreateSerializer, TaskUpdateSerializer,  GetTaskSerializer, UpdateEvaluation, GetCommentSerializer, UpdateCommentSerializer, CreateCommentSerializer, CreateEvaluation
from task.exeptions import TaskConflictError

from django.shortcuts import get_object_or_404

from task.utils import is_int_or_valid_error


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
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
        """Просмотр своих Task"""
        user_worker = request.user.worker

        tasks = Task.objects.filter(executor=user_worker)
        serializer = self.get_serializer(tasks, many=True)
        
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.worker)

    def perform_update(self, serializer):
        executor = serializer.validated_data.get("executor")
        status = serializer.validated_data.get("status")
        instance = self.get_object()

        if hasattr(instance, "evaluation"):
            if executor and executor != instance.executor:
                raise TaskConflictError(detail={"task_update_conflict": "Ошибка. Нельзя изменить исполнителя(executor) для оцененной и завершенной задачи."})
            if status and status != instance.status:
                raise TaskConflictError(detail={"task_update_conflict": "Ошибка. Нельзя изменить статус(status) для оцененной и завершенной задачи."})
        serializer.save()

    
class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete", "options", "head")
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
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
        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)

        task = get_object_or_404(Task, pk=task_pk)

        serializer.save(creator=self.request.user.worker, task=task)
    
    def get_queryset(self):
        queryset = super().get_queryset()

        task_pk = self.kwargs.get("task_pk")
        task_pk = is_int_or_valid_error(num_check=task_pk)
        get_object_or_404(Task, pk=task_pk)

        comments = queryset.filter(task=task_pk)
        return comments


class EvaluationViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Evaluation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        request.data["task"] = kwargs.get("task_pk")
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        task = serializer.validated_data.get("task")
        from_worker = self.request.user.worker
        if not task.executor:
            raise serializers.ValidationError({"evaluation": "Задача, за которую выставляется оценка, не имеет назначенного исполнителя."})
        elif task.status != Task.StatusTask.DONE:
            raise serializers.ValidationError({"evaluation": "Задача, за которую выставляется оценка, должна быть в статусе выполнена."})
        serializer.save(to_worker=task.executor, from_worker=from_worker)

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CreateEvaluation
        elif self.action == "partial_update":
            self.serializer_class = UpdateEvaluation
        return self.serializer_class
    
