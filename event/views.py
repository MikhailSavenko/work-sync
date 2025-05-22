from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from event.models import Meeting
from event.serializers import MeetingSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        current_user = self.request.user.worker
        serializer.save(creator=current_user)

