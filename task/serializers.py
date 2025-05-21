from rest_framework import serializers

from task.models import Comment, Evaluation, Task
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
    status = serializers.ReadOnlyField(source="get_status_display")

    class Meta:

        model = Task
        fields = ("id", "title", "description", "status", "deadline", "executor")
        extra_kwargs = {
            "executor": {"help_text": "id"},
            "deadline":  {"help_text": "YYYY-MM-DD"},
            "status":  {"help_text": "OP|AW|DN"}
        }


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для обновления Task"""
    class Meta:

        model = Task
        fields = ("id", "title", "description", "deadline", "status", "executor")
        extra_kwargs = {
            "executor": {"help_text": "id"},
            "deadline":  {"help_text": "YYYY-MM-DD"},
            "status":  {"help_text": "OP|AW|DN"}
        }
        

class GetCommentSerializer(serializers.ModelSerializer):
    """Получить коммент сериалайзер"""

    class Meta:
        model = Comment
        fields = ("id", "task", "text", "creator", "created_at", "updated_at")


class CreateCommentSerializer(serializers.ModelSerializer):
    """Создать комменты сериалайзер"""

    class Meta:
        model = Comment
        fields = ("id", "task", "text", "created_at", "updated_at")


class UpdateCommentSerializer(serializers.ModelSerializer):
    """Обновить коммент сериалайзер"""

    class Meta:
        model = Comment
        fields = ("text", )


class CreateEvaluation(serializers.ModelSerializer):
    """
    Создание оценки на Task для executor
    score - min 1 max 5
    task - id Task на который оставляют оценку, берем из kwarsg
    to_worker - кому оценка, id берем из Task.executor
    from_worker - кто выставляет, берем из request.user.worker
    """

    class Meta:
        model = Evaluation
        fields = ("id", "score", "task")


class UpdateEvaluation(serializers.ModelSerializer):
    """
    Обновление оценки на Task для executor
    score - min 1 max 5
    task - id Task на который оставляют оценку, берем из kwarsg
    to_worker - кому оценка, id берем из Task.executor
    from_worker - кто выставляет, берем из request.user.worker
    """

    class Meta:
        model = Evaluation
        fields = ("score",)