from rest_framework import serializers

from event.models import Meeting
from account.models import Worker
from event.services.meeting import validate_workers_and_include_creator, check_if_datetime_is_free
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
    datetime = serializers.DateTimeField(input_formats=("%Y-%m-%dT%H:%M",))

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")

    def validate(self, data):
        creator = self.context["request"].user.worker
        workers = data.get("workers")

        workers = validate_workers_and_include_creator(creator=creator, workers=workers)

        data["workers"] = workers

        # Проверка наложения встреч приглашенных участников
        for worker in workers:
            if not check_if_datetime_is_free(worker=worker, check_date=data["datetime"]):
                raise serializers.ValidationError(f"В это время у пользователя {worker.user.email} уже назначена встреча!")
        
        return data

    def validate_datetime(self, value):
        """Проверка даты и времени. Дату и время в прошлом назначить нельзя"""
        date_now = timezone.now()

        if value < date_now:
            raise serializers.ValidationError("Дата и время встречи не может быть в прошлом.")
        
        print(value)
        
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