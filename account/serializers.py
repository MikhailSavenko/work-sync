from rest_framework import serializers
from account.models import Worker, User


class WorkerSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Worker
        fields = ("team", "role")


class UserMeSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'worker')


class UserSerializer(UserMeSerializer):
    pass