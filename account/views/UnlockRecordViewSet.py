from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import UnlockRecord
from account.serializers import BasicUnlockRecordSerializer, UnlockRecordSerializer

from .permissions import IsAdminUserOrReadOnly, IsSelfOrReadOnly

from django.shortcuts import get_object_or_404

class UnlockRecordViewSet(viewsets.ModelViewSet):
    queryset = UnlockRecord.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UnlockRecordSerializer
        else:
            return BasicUnlockRecordSerializer
