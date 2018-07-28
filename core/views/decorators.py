from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from budget.models import Item
from core.models import Requirement, Fund


def check_submitted(requirement, kwargs):
    pk = kwargs['requirement_pk'] if 'requirement_pk' in kwargs else kwargs['pk']
    requirement = get_object_or_404(Requirement.objects.all(), pk=pk)
    return requirement.is_submitted


def lock_if_submitted(wrapped):
    def inner(self, request, *args, **kwargs):
        if check_submitted(requirement, kwargs):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': 'Cannot update submitted requirements.'})
        else:
            return wrapped(self, request, *args, **kwargs)
    return inner


def pass_if_submitted(wrapped):
    def inner(self, request, *args, **kwargs):
        if not check_submitted(requirement, kwargs):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': 'Cannot review not-submitted requirements.'})
        else:
            return wrapped(self, request, *args, **kwargs)
    return inner
