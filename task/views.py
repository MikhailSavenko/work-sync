from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from task.doc.schemas import TaskAutoSchema
from task.models import Evaluation, Task, Comment
from task.serializers import TaskCreateSerializer, TaskUpdateSerializer,  GetTaskSerializer, UpdateEvaluation, GetCommentSerializer, UpdateCommentSerializer, CreateCommentSerializer, CreateEvaluation


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
    swagger_schema = TaskAutoSchema

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
                raise serializers.ValidationError({"task_update_executor": "Ошибка. Нельзя изменить исполнителя для оцененной и завершенной задачи."})
            if status and status != instance.status:
                raise serializers.ValidationError({"task_update_status": "Ошибка. Нельзя изменить статус для оцененной и завершенной задачи."})
        serializer.save()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = TaskCreateSerializer
        elif self.action in ["retrieve", "list", "me"]:
            self.serializer_class = GetTaskSerializer
        elif self.action in ["update", "partial_update"]:
            self.serializer_class = TaskUpdateSerializer
        return self.serializer_class

    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["task"] = kwargs.get("task_pk")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.worker)

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CreateCommentSerializer
        elif self.action == "retrieve":
            self.serializer_class = GetCommentSerializer
        elif self.action == "list":
            self.serializer_class = GetCommentSerializer
        elif self.action == "partial_update":
            self.serializer_class = UpdateCommentSerializer
        return self.serializer_class


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
    
