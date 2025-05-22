from rest_framework import viewsets
from rest_framework import mixins

from account.serializers import TeamSerializer, WorkerGetSerializer
from account.models import Team, Worker


class TeamViewSet(viewsets.ModelViewSet):
    """Представление для Team"""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    # будет доступен admin_team


class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    serializer_class = WorkerGetSerializer
    queryset = Worker.objects.all()

