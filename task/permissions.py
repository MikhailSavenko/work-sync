from rest_framework.permissions import SAFE_METHODS, BasePermission

from account.models import Worker
from common.variables import FORBIDDEN_403_RUSSIAN


class IsCreatorAdminManagerOrReadOnly(BasePermission):
    """Создатель - Админ команды/Менеджер или чтение"""

    message = FORBIDDEN_403_RUSSIAN

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.worker.role in [Worker.Role.ADMIN_TEAM, Worker.Role.MANAGER]

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user.worker


class IsCreatorOrReadOnly(BasePermission):
    message = FORBIDDEN_403_RUSSIAN

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user.worker


class IsCreatorAdminManager(BasePermission):
    message = FORBIDDEN_403_RUSSIAN

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.worker.role in [Worker.Role.ADMIN_TEAM, Worker.Role.MANAGER]

    def has_object_permission(self, request, view, obj):
        return obj.from_worker == request.user.worker
