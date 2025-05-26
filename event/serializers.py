from rest_framework import serializers

from event.models import Meeting
from account.models import Worker


class MeetingSerializer(serializers.ModelSerializer):
    """
    Сериалайзер встречи

    datetime - время и дата
    creator - из request.user.worker 
    workers: list - список id приглашенных сотрудников
    """
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    workers = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), many=True)

    class Meta:
        model = Meeting
        fields = ("id", "description", "datetime", "creator", "workers")

    