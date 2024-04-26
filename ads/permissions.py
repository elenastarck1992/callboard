from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс для роли создателя"""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки принадлежности объявления создателю"""
        return request.user == obj.author


class IsAdmin(BasePermission):
    """Класс для роли администратора"""

    def has_permission(self, request, view):
        """Метод для определения принадлежности к группе администраторов"""
        if request.user.groups.filter(name="Admin").exists():
            return True
        return False
