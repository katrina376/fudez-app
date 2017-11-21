from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import User
from account.serializers import BasicUserSerializer, UserSerializer

from .permissions import IsAdminUserOrReadOnly, IsSelfOrReadOnly

from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializer
        else:
            return BasicUserSerializer

    @detail_route(methods=['patch'], permission_classes=[IsSelfOrReadOnly], url_path='update-info')
    def update_info(self, request, pk=None):
        user = request.user
        return Response()
