from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import UnlockRecord
from account.serializers import UnlockRecordSerializer, FullUnlockRecordSerializer

from .permissions import IsAdminUserOrReadOnly


class UnlockRecordViewSet(viewsets.ModelViewSet):
    queryset = UnlockRecord.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return FullUnlockRecordSerializer
        else:
            return UnlockRecordSerializer
