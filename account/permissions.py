from rest_framework.permissions import BasePermission, SAFE_METHODS

from account.models import Worker

MESSAGE_403 = "У вас недостаточно прав для выполнения этого действия."

class IsAdminTeamOrReadOnly(BasePermission):
    message = MESSAGE_403

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.worker.role == Worker.Role.ADMIN_TEAM

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.creator == request.user.worker


class IsAdminTeam(BasePermission):
    message = MESSAGE_403

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True
        
        return request.user.worker.role == Worker.Role.ADMIN_TEAM
    