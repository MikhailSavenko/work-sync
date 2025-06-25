from rest_framework.permissions import SAFE_METHODS, BasePermission

from common.permissions import MESSAGE_403


class IsOwnerOrReadOnly(BasePermission):
    message = MESSAGE_403

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user.worker
