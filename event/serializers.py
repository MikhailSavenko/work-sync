from rest_framework import serializers

from event.exceptions import MeetingConflictError
from event.models import Meeting
from account.models import Worker
from event.services.meeting import validate_workers_and_include_creator, is_datetime_available
from task.serializers import WorkerNameSerializer
from django.utils import timezone


class MeetingCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер встречи - Создание

    datetime - время и дата
    creator - из request.user.worker
    workers: list - список id приглашенных сотрудников
    description - описание встречи
    """
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    workers = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), many=True, help_text="Список ID приглашенных сотрудников")
    datetime = serializers.DateTimeField(input_formats=("%Y-%m-%dT%H:%M",), 
                                         help_text="Формат: YYYY-MM-DDTHH:MM")

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")

    def validate(self, data):
        data = super().validate(data)

        request = self.context["request"]
        creator = request.user.worker
        workers = data.get("workers")

        # Валидация участников
        data["workers"] = validate_workers_and_include_creator(creator=creator, workers=workers)

        # Проверка наложения встреч приглашенных участников
        meeting_id = None
        if self.context["request"].method == "PUT":
            meeting_id = self.instance.pk if self.instance else None
        
        for worker in data["workers"]:
            print(meeting_id)
            print("Тут")
            if not is_datetime_available(worker=worker, check_date=data["datetime"], meeting_id=meeting_id):
                raise MeetingConflictError(f"{worker.user.email} уже имеет встречу на дату: {data["datetime"]}")
        
        return data

    def validate_datetime(self, value):
        """Проверка что дата не в прошлом"""
        date_now = timezone.now()

        if value < date_now:
            raise serializers.ValidationError("Дата и время встречи не может быть в прошлом.")
        
        return value


class MeetingGetSerializer(serializers.ModelSerializer):
    """
    Сериалайзер встречи - Просмотр

    datetime - время и дата
    creator - из request.user.worker 
    workers: list - список id приглашенных сотрудников
    description - описание встречи
    """
    creator = serializers.PrimaryKeyRelatedField(read_only=True) # избыточно
    workers = WorkerNameSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")