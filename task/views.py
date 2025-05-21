from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from task.models import Task, Comment
from task.serializers import CreateTaskSerializer, GetTaskSerializer, UpdateTaskSerializer, GetCommentSerializer, UpdateCommentSerializer, CreateCommentSerializer


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
        elif self.action == "update":
            self.serializer_class = UpdateCommentSerializer
        elif self.action == "partial_update":
            self.serializer_class = UpdateCommentSerializer
        return self.serializer_class