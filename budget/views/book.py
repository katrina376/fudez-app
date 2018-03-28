from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from rest_framework import status
from rest_framework.response import Response

from account.models import Department
from budget.models import Book
from budget.serializers import FullBookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = FullBookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Book.objects.all()

        if 'department' in self.request.query_params:
            pk = self.request.query_params['department']
            departmemt = get_object_or_404(Department.objects.all(), pk=pk)
            queryset = queryset.filter(projects__in=departmemt.projects.all())

        queryset = self.get_serializer_class().setup_eager_loading(queryset)

        return queryset
