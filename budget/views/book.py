from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from account.models import Department
from budget.models import Book
from budget.serializers import FullBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = FullBookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if 'department' in self.request.query_params:
            pk = self.request.query_params['department']
            departmemt = get_object_or_404(Department.objects.all(), pk=pk)
            return Book.objects.filter(projects__in=departmemt.projects.all())
        else:
            return Book.objects.all()
