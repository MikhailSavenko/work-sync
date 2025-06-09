from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from event.models import Meeting
from event.doc.schemas import MeetingAutoSchema
from event.serializers import MeetingGetSerializer, MeetingCreateUpdateSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    """
    API для работы с встречами.
    
    Позволяет:
    - Создавать новые встречи
    - Просматривать/редактировать существующие
    - Отменять встречи
    - Получать список предстоящих или завершенных встреч текущего пользователя
    """
    http_method_names = ["get", "post", "put", "delete", "options", "head"]
    permission_classes = (IsAuthenticated,)
    queryset = Meeting.objects.all()
    serializer_class = {
        "list": MeetingGetSerializer,
        "retrieve": MeetingGetSerializer,
        "me": MeetingGetSerializer,
        "update": MeetingCreateUpdateSerializer,
        "create": MeetingCreateUpdateSerializer,
    }
    swagger_schema = MeetingAutoSchema

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, MeetingGetSerializer)
    
    def perform_create(self, serializer):
        current_user = self.request.user.worker
        serializer.save(creator=current_user)
    
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user_worker = request.user.worker
        done_param = request.query_params.get("done", "0")
        
        if done_param not in ("0", "1"):
            return Response(
                {"detail": "Парамтер 'done' может быть 0 или 1"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        queryset = super().get_queryset()

        if done_param == "1":
            meetings = queryset.filter(workers=user_worker)
        elif done_param == "0":
            now = timezone.now()
            meetings = queryset.filter(workers=user_worker, datetime__gt=now)
        
        serializer = self.get_serializer_class()
        serializer = serializer(meetings, many=True)

        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # по сути это можно будет убрать, когда я напишу нормлаьные permission
        if instance.creator != request.user.worker:
            return Response({"detail": "Отмена встречи возможна только ее создателем."}, status=status.HTTP_403_FORBIDDEN)
        
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)