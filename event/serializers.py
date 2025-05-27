from rest_framework import serializers

from event.models import Meeting
from account.models import Worker
from task.serializers import WorkerNameSerializer
from django.utils import timezone


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

    def validate(self, data):
        creator = self.context["request"].user.worker
        workers = data.get("workers")

        if not workers:
            raise serializers.ValidationError("Укажите хотя бы одного сотрудника для встречи.")
        
        workers = list(workers)

        if creator not in workers:
            workers.append(creator)
        
        if len(set(workers)) < 2:
            raise serializers.ValidationError("Встреча должна включать минимум двух участников.")
        
        data["workers"] = workers
        return data

    def validate_datetime(self, value):
        """Создавать встречи в прошллом нельзя"""
        date_now = timezone.now()
        if value < date_now:
            raise serializers.ValidationError("Дата встречи не может быть в прошлом.")
        return value


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