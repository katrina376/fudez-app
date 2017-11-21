from rest_framework import viewsets, permissions

from django.contrib.auth import get_user_model

class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user

class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            admin_kinds = [get_user_model().CHIEF, get_user_model().ENGINEER]
            return request.user.kind in admin_kinds

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.department == obj.department
