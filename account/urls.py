from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views import TeamViewSet, UserViewSet, WorkerViewSet, TokenObtainPairView, TokenBlacklistView, TokenRefreshView, TokenVerifyView


router = DefaultRouter()

app_name = "account"


router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"workers", WorkerViewSet, basename="worker") # тут добавлять NestedRouter и workers/meetings

urlpatterns = [
    path("auth/users/register/", UserViewSet.as_view({"post": "create"}), name="register"), 
    path("auth/users/me/",  UserViewSet.as_view({'put': 'me', 'delete': 'me'}), name="user_me"),
    path("auth/jwt/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("auth/jwt/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),

    path("", include(router.urls)),

    
    
]
