from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import User
from account.serializers import UserSerializer, SimpleUserSerializer, FullUserSerializer, UserOverwriteSerializer

from .permissions import IsAdminUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            if self.action == 'list':
                return SimpleUserSerializer
            else:
                return FullUserSerializer
        else:
            if self.request.method.lower() == 'post':
                return UserSerializer
            else:
                return UserOverwriteSerializer
