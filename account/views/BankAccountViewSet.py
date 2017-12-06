from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from account.models import BankAccount
from account.serializers import BankAccountSerializer, FullBankAccountSerializer

from .permissions import IsMember


class BankAccountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsMember)
    parent = 'department'

    @property
    def parent_pk(self):
        if '{}_pk'.format(self.parent) in self.kwargs:
            return self.kwargs['{}_pk'.format(self.parent)]
        else:
            return None

    def initial(self, request, *args, **kwargs):
        if self.request.method not in permissions.SAFE_METHODS:
            data = self.request.data
            data[self.parent] = self.parent_pk
            request._request.POST = data
        return super(BankAccountViewSet, self).initial(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return FullBankAccountSerializer
        else:
            return BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.filter(department__pk=self.parent_pk)
