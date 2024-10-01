# api/permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение только владельцу объекта для изменений.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение для любых запросов
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на изменение только владельцу
        return obj.owner == request.user
