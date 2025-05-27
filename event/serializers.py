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

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")

    def validate(self, data):
        creator = self.context["request"].user.worker
        workers = data.get("workers")

        workers = validate_workers_and_include_creator(creator=creator, workers=workers)
        
        data["workers"] = workers
        
        return data

    def validate_datetime(self, value):
        current_worker = self.context["request"].user.worker
        date_now = timezone.now()
        
        # Проверка на прошлое
        if value < date_now:
            raise serializers.ValidationError("Дата встречи не может быть в прошлом.")
        
        # Проверка наложения встреч
        if not check_if_datetime_is_free(worker=current_worker, check_date=value):
            raise serializers.ValidationError("В это время у вас уже назначена встреча!")
        
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