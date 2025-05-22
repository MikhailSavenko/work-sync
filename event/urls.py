from django.urls import path, include
from rest_framework.routers import DefaultRouter

from event.views import MeetingViewSet

app_name = "event"

router = DefaultRouter()
router.register(r"meetings", MeetingViewSet, basename="meeting")

urlpatterns = [
    path("", include(router.urls)),
]