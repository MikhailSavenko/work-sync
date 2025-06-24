from rest_framework import serializers
from account.models import Worker, User, Team
from task.serializers import GetTaskSerializer
from event.serializers import MeetingGetSerializer


class WorkerCalendarResponseSerializer(serializers.Serializer):
    """Serializer для календаря событий"""
    date = serializers.DateField()
    meetings = MeetingGetSerializer(many=True)
    tasks = GetTaskSerializer(many=True)
    table = serializers.ListField(child=serializers.CharField())


class WorkerEvaluationResponseSerializer(serializers.Serializer):
    """Serializer для просмотра средней оценки сотрудника за период"""
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    average_score = serializers.FloatField(help_text="Средняя оценка сотрудника за период")
    evaluations_count = serializers.IntegerField(help_text="Количество оценок")


class TeamShortSerializer(serializers.ModelSerializer):
    """Вложенный сериалайзер для Worker.team"""
    class Meta:
        model = Team
        fields = ("id", "title")


class WorkerGetSerializer(serializers.ModelSerializer):
    """Сериалайзер Сотрудника просмотра с полями пользователя"""
    user_id = serializers.IntegerField(source="user.id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    role = serializers.CharField(source='get_role_display', read_only=True)
    team = TeamShortSerializer()

    class Meta:
        model = Worker
        fields = ("id", "team", "role", "user_id", "first_name", "last_name", "email")


class WorkerUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер обновления роли для сотрудника"""
    class Meta:
        model = Worker
        fields = ("role",)
        extra_kwargs = {
            "role": {"help_text": "NM - Пользователь |MG - Менеджер |AT - Админ"}
        }


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для users/me(put) и users/register(post)"""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания/обновления Тeam"""
    workers = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "title", "creator", "description", "workers", "created_at", "updated_at")


class TeamWorkerGetSerializer(serializers.ModelSerializer):
    """Сериалайзер cотрудника для вложения в TeamGetSerializer"""
    user_id = serializers.IntegerField(source="user.id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Worker
        fields = ("id", "role", "email", "user_id", "first_name", "last_name")


class TeamGetSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра Тeam"""
    workers = TeamWorkerGetSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "title", "creator", "description", "workers", "created_at", "updated_at")