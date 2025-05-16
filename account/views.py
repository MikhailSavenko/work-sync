from rest_framework import viewsets

from account.serializers import TeamSerializer
from account.models import Team


class TeamViewSet(viewsets.ModelViewSet):
    """Представление для Team"""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    # будет доступен admin_team



