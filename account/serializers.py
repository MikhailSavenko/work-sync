from rest_framework import serializers
from account.models import Worker, User, Team


class WorkerSerializer(serializers.ModelSerializer):
    """Сериалайзер Сотрудника для вложения в UserMeSerializer"""
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Worker
        fields = ("id", "team", "role")


# Здесь вывести всю инфу по воркеру и user инфу
class WorkerGetSerializer(serializers.ModelSerializer):
    """Сериалайзер Сотрудника"""
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Worker
        fields = ("id", "team", "role", "user_id")


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для users/me(put) и users/register(post)"""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class TeamSerializer(serializers.ModelSerializer):
    """Сериалайзер для управления Тeam"""
    # workers = UserMeSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "title", "description", "workers")