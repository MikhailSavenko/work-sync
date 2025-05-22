from rest_framework import serializers
from account.models import Worker, User, Team


class WorkerSerializer(serializers.ModelSerializer):
    """Сериалайзер Сотрудника"""
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Worker
        fields = ("id", "team", "role")


class UserMeSerializer(serializers.ModelSerializer):
    """Сериалайзер для users/me"""
    worker = WorkerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "worker")


class UserSerializer(UserMeSerializer):
    pass


class TeamSerializer(serializers.ModelSerializer):
    """Сериалайзер для управления Тeam"""
    workers = UserMeSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "title", "description", "workers")