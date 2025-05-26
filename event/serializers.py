from rest_framework import serializers

from event.models import Meeting
from account.models import Worker
from task.serializers import WorkerNameSerializer


class MeetingCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер встречи - Создание

    datetime - время и дата
    creator - из request.user.worker 
    workers: list - список id приглашенных сотрудников
    description - описание встречи
    """
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    workers = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), many=True)

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")


class MeetingGetSerializer(serializers.ModelSerializer):
    """
    Сериалайзер встречи - Просмотр

    datetime - время и дата
    creator - из request.user.worker 
    workers: list - список id приглашенных сотрудников
    description - описание встречи
    """
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    workers = WorkerNameSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")