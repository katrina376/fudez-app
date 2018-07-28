from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from core.models import Fund, Requirement
from core.serializers import FundSerializer, FullFundSerializer

from .decorators import lock_if_submitted
from .permissions import IsRelatedOrReadOnly, IsOwnerOrReadOnly


class FundViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    parent = 'requirement'
    parent_lookup = '{}_pk'.format(parent)

    @property
    def parent_pk(self):
        if self.parent_lookup in self.kwargs:
            return int(self.kwargs[self.parent_lookup])
        else:
            return None

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return FullFundSerializer
        else:
            return FundSerializer

    def get_serializer_context(self):
        return {self.parent: self.parent_pk}

    def get_queryset(self):
        return Fund.objects.filter(requirement__pk=self.parent_pk)

    @lock_if_submitted
    def create(self, *args, **kwargs):
        return super(FundViewSet, self).create(*args, **kwargs)

    @lock_if_submitted
    def update(self, *args, **kwargs):
        return super(FundViewSet, self).update(*args, **kwargs)

    @lock_if_submitted
    def partial_update(self, *args, **kwargs):
        return super(FundViewSet, self).partial_update(*args, **kwargs)

    @lock_if_submitted
    def destroy(self, *args, **kwargs):
        return super(FundViewSet, self).destroy(*args, **kwargs)
