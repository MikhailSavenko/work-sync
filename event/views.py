from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from event.models import Meeting
from event.serializers import MeetingGetSerializer, MeetingCreateUpdateSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    """Представление Встречи. Создание/Отмена/Получение/Свои встречи"""
    permission_classes = (IsAuthenticated,)
    queryset = Meeting.objects.all()

    serializer_class = {
        "list": MeetingGetSerializer,
        "retrieve": MeetingGetSerializer,
        "me": MeetingGetSerializer,
        "update": MeetingCreateUpdateSerializer,
        "create": MeetingCreateUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, MeetingGetSerializer)
    
    def perform_create(self, serializer):
        current_user = self.request.user.worker
        serializer.save(creator=current_user)
    
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user_worker = request.user.worker
        done_param = request.query_params.get("done", "0")
        print(done_param)
        
        if done_param not in ("0", "1"):
            return Response(
                {"error": "Парамтер 'done' может быть 0 или 1"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        if done_param == "1":
            meetings = Meeting.objects.filter(workers=user_worker)
        elif done_param == "0":
            now = timezone.now()
            meetings = Meeting.objects.filter(workers=user_worker, datetime__gt=now)
        
        serializer = self.get_serializer_class()
        serializer = serializer(meetings, many=True)

        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.creator != request.user.worker:
            return Response({"detail": "Отмена встречи возможна только ее создателем."}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)