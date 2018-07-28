from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from account.models import User


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            admin_kinds = [get_user_model().CHIEF, get_user_model().ENGINEER]
            return request.user.kind in admin_kinds


class IsRelatedOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('IsRelatedOrReadOnly')
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.kind == get_user_model().DEPARTMENT:
                return request.user.department == obj.department
            elif request.user.kind == get_user_model().PRESIDENT:
                return request.user.department.kind == obj.department.kind
            elif request.user.kind == get_user_model().STAFF:
                departments = request.user.assist_departments.all()
                return obj.department in departments
            elif request.user.kind == get_user_model().CHIEF:
                return True
            else:
                return False


class IsReviewer(permissions.BasePermission):
    def has_permission(self, request, view):
        print('IsReviewer')
        reviewer_kinds = [get_user_model().PRESIDENT, get_user_model().STAFF, get_user_model().CHIEF]
        return request.user.kind in reviewer_kinds

    def has_object_permission(self, request, view, obj):
        print('IsReviewer')
        if request.user.kind == get_user_model().PRESIDENT:
            return request.user.department.kind == obj.department.kind
        elif request.user.kind == get_user_model().STAFF:
            departments = request.user.assist_departments.all()
            return obj.department in departments
        elif request.user.kind == get_user_model().CHIEF:
            return True
        else:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('IsOwnerOrReadOnly')
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.applicant == request.user


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.department.pk == int(view.kwargs['department_pk'])
        except:
            return False


class IsApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.kind == get_user_model().DEPARTMENT
