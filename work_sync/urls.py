from django.contrib import admin
from django.urls import path, include

VERSION = "v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"api/{VERSION}/", include("account.urls", namespace="account")),
    path(f"api/{VERSION}/", include("task.urls", namespace="task")),
    path(f"api/{VERSION}/", include("event.urls", namespace="event")),
]
