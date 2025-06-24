from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Work sync API",
        default_version="v1",
        description="API для синхронизации работы внутри компании",
        contact=openapi.Contact(email="mi47sav@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
VERSION = "v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"api/{VERSION}/", include("account.urls", namespace="account")),
    path(f"api/{VERSION}/", include("task.urls", namespace="task")),
    path(f"api/{VERSION}/", include("event.urls", namespace="event")),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
