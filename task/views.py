from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from task.models import Task
from task.serializers import CreateTaskSerializer, GetTaskSerializer, UpdateTaskSerializer


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
    
