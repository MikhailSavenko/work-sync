from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView, TokenVerifyView
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from account.views import TeamViewSet, WorkerViewSet


router = DefaultRouter()

app_name = "account"


router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"workers", WorkerViewSet, basename="worker")

urlpatterns = [
    path("users/", UserViewSet.as_view({"get": "list"}), name="users"),
    path("users/me/",  UserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me', 'delete': 'me'}), name="user_me"), # разрешен GET PUT PATH DELETE
    path("users/<int:id>/", UserViewSet.as_view({"get": "retrieve"}), name="user_by_id"),
    path("auth/users/register/", UserViewSet.as_view({"post": "create"}), name="register"),
    path("auth/jwt/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("auth/jwt/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("", include(router.urls))

]
