from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import Department, User
from account.serializers import BasicDepartmentSerializer, DepartmentSerializer

from .permissions import IsAdminUserOrReadOnly

from django.shortcuts import get_object_or_404

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return DepartmentSerializer
        else:
            return BasicDepartmentSerializer

    @detail_route(methods=['patch'], url_path='set-assistant')
    def set_assistant(self, request, pk=None):
        department = get_object_or_404(self.queryset, pk=pk)
        user_pk = request.data['user']
        assistant = get_object_or_404(User.objects.all(), pk=user_pk)
        department.assistant = assistant
        department.save()
        return Response(status=status.HTTP_200_OK,
                        data=self.get_serializer(department).data)
