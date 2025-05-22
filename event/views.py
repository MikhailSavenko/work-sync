from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from event.models import Meeting
from event.serializers import MeetingSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def perform_create(self, serializer):
        current_user = self.request.user.worker
        serializer.save(creator=current_user)
    
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user_worker = request.user.worker
        now = timezone.now()

        meetings = Meeting.objects.filter(workers=user_worker, datetime__gt=now)
        serializer = self.serializer_class(meetings, many=True)

        return Response(serializer.data)
        
