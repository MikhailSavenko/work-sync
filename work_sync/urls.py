from django.contrib import admin
from django.urls import path, include

VERSION = "v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"api/{VERSION}/", include("account.urls", namespace="account"))
]
