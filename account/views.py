from rest_framework import viewsets
from rest_framework import mixins

from account.serializers import TeamCreateUpdateSerializer, WorkerGetSerializer, TeamGetSerializer
from account.models import Team, Worker


class TeamViewSet(viewsets.ModelViewSet):
    """Представление для Team"""
    queryset = Team.objects.all()

    # будет доступен admin_team

    def get_serializer_class(self):
        if self.action == "update":
            self.serializer_class = TeamCreateUpdateSerializer
        elif self.action == "retrieve":
            self.serializer_class = TeamGetSerializer
        elif self.action == "list":
            self.serializer_class = TeamGetSerializer
        return self.serializer_class


class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin):
    serializer_class = WorkerGetSerializer
    queryset = Worker.objects.all()

    