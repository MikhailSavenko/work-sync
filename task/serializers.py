from django.utils import timezone
from rest_framework import serializers

from account.models import Worker
from task.models import Comment, Evaluation, Task


class WorkerNameSerializer(serializers.ModelSerializer):
    """Сериалайзер полей Сотрудника и его имени в Профиле"""

    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    role = serializers.CharField(source="get_role_display", read_only=True)
    team = serializers.SerializerMethodField()

    class Meta:

        model = Worker
        fields = ("id", "full_name", "role", "team")

    def get_team(self, obj):
        return obj.team.title if obj.team else "Без команды"


class GetTaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения Task"""

    status = serializers.CharField(source="get_status_display", read_only=True)
    executor = WorkerNameSerializer(read_only=True)
    creator = WorkerNameSerializer(read_only=True)

    evaluation = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "deadline",
            "status",
            "executor",
            "creator",
            "evaluation",
            "created_at",
            "updated_at",
        )

    def get_evaluation(self, obj: Task):
        current_worker = self.context.get("request").user.worker
        # Покажем оценку менеджеру кто назначил задачу и самому исполнителю
        if (hasattr(obj, "evaluation") and obj.executor and obj.executor == current_worker) or (
            hasattr(obj, "evaluation") and obj.creator and obj.creator == current_worker
        ):
            evalu_serializer = EvaluationSerializer(obj.evaluation)
            return evalu_serializer.data
        return None


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания Task"""

    status = serializers.ReadOnlyField(
        source="get_status_display", help_text="OP - открыт |AW - в работе |DN - завершен"
    )
    deadline = serializers.DateTimeField(input_formats=("%Y-%m-%dT%H:%M",), help_text="Формат: YYYY-MM-DDTHH:MM")
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Task
        fields = ("id", "title", "description", "status", "deadline", "executor", "creator")
        extra_kwargs = {"executor": {"help_text": "id исполнителя, может быть назначен позже"}}

    def validate_deadline(self, value):
        """Проверка что дата не в прошлом"""
        date_now = timezone.now()

        if value < date_now:
            raise serializers.ValidationError("Дэдлайн не может быть в прошлом.")

        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер для  обновления Task"""

    status = serializers.ChoiceField(choices=Task.StatusTask, help_text="OP - открыт |AW - в работе |DN - завершен")
    deadline = serializers.DateTimeField(input_formats=("%Y-%m-%dT%H:%M",), help_text="Формат: YYYY-MM-DDTHH:MM")
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = Task
        fields = ("id", "title", "description", "status", "deadline", "executor", "creator")
        extra_kwargs = {
            "executor": {"help_text": "id исполнителя, может быть назначен позже"},
            "deadline": {"help_text": "YYYY-MM-DDTHH:MM"},
        }

    def validate_deadline(self, value):
        """Проверка что дата не в прошлом"""
        date_now = timezone.now()

        if value < date_now:
            raise serializers.ValidationError("Дэдлайн не может быть в прошлом.")

        return value


class GetCommentSerializer(serializers.ModelSerializer):
    """Получить коммент сериалайзер"""

    class Meta:
        model = Comment
        fields = ("id", "task", "text", "creator", "created_at", "updated_at")


class CreateCommentSerializer(serializers.ModelSerializer):
    """Создать комменты сериалайзер"""

    task = serializers.PrimaryKeyRelatedField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "task", "creator", "created_at", "updated_at")


class UpdateCommentSerializer(serializers.ModelSerializer):
    """Обновить коммент сериалайзер"""

    class Meta:
        model = Comment
        fields = ("text",)


class CreateEvaluation(serializers.ModelSerializer):
    """
    Создание оценки на Task для executor
    score - min 1 max 5
    task - id Task на который оставляют оценку, берем из kwarsg
    to_worker - кому оценка, id берем из Task.executor
    from_worker - кто выставляет, берем из request.user.worker
    """

    task = serializers.PrimaryKeyRelatedField(read_only=True)

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


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ("id", "score", "from_worker", "to_worker")
