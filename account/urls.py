from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView
app_name = "account"

urlpatterns = [
    path("auth/jwt/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
