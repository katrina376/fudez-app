from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from account.models import BankAccount
from account.serializers import BankAccountSerializer, FullBankAccountSerializer

from .permissions import IsMember


class BankAccountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsMember)
    parent = 'department'
    parent_lookup = '{}_pk'.format(parent)

    @property
    def parent_pk(self):
        if self.parent_lookup in self.kwargs:
            return int(self.kwargs[self.parent_lookup])
        else:
            return None

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return FullBankAccountSerializer
        else:
            return BankAccountSerializer

    def get_serializer_context(self):
        return {self.parent: self.parent_pk}

    def get_queryset(self):
        return BankAccount.objects.filter(department__pk=self.parent_pk)
