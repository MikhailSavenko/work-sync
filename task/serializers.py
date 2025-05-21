from rest_framework import serializers

from task.models import Comment, Task
from account.models import Worker


class WorkerNameSerializer(serializers.ModelSerializer):
    """Сериалайзер полей Сотрудника и его имени в Профиле"""
    worker = serializers.CharField(source="user.get_full_name", read_only=True)
    role = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:

        model = Worker
        fields = ("worker", "role", "team")


class GetTaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения Task"""
    status = serializers.CharField(source="get_status_display", read_only=True)
    executor = WorkerNameSerializer(read_only=True)
    creator = WorkerNameSerializer(read_only=True)

    class Meta:

        model = Task
        fields = ("id", "title", "description", "deadline", "status", "executor", "creator", "created_at", "updated_at")


class CreateTaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания Task"""
    class Meta:

        model = Task
        fields = ("title", "description", "deadline", "status", "executor")
        extra_kwargs = {
            "executor": {"help_text": "id"},
            "deadline":  {"help_text": "YYYY-MM-DD"},
            "status":  {"help_text": "OP|AW|DN"}
        }


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления Task"""
    class Meta:

        model = Task
        fields = ("title", "description", "deadline", "status", "executor")
        extra_kwargs = {
            "executor": {"help_text": "id"},
            "deadline":  {"help_text": "YYYY-MM-DD"},
            "status":  {"help_text": "OP|AW|DN"}
        }
        

class CommentSerializer(serializers.ModelSerializer):
    """Комменты сериалайзер"""

    class Meta:
        model = Comment
        fields = ("id", "task", "text", "creator", "created_at", "updated_at")