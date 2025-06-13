from rest_framework.permissions import BasePermission, SAFE_METHODS

from common.permissions import MESSAGE_403
from account.models import Worker


class IsCreatorAdminManagerOrReadOnly(BasePermission):
    """Создатель - Админ команды/Менеджер или чтение"""
    message = MESSAGE_403

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
