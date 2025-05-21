from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from task.models import Evaluation, Task, Comment
from task.serializers import CreateTaskSerializer, GetTaskSerializer, UpdateEvaluation, UpdateTaskSerializer, GetCommentSerializer, UpdateCommentSerializer, CreateCommentSerializer, CreateEvaluation
from rest_framework import mixins


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.worker)

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CreateTaskSerializer
        elif self.action == "retrieve":
            self.serializer_class = GetTaskSerializer
        elif self.action == "list":
            self.serializer_class = GetTaskSerializer
        elif self.action == "update":
            self.serializer_class = UpdateTaskSerializer
        elif self.action == "partial_update":
            self.serializer_class = UpdateTaskSerializer
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
    
