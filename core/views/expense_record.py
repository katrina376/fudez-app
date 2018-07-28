from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core.models import ExpenseRecord
from core.serializers import ExpenseRecordSerializer, FullExpenseRecordSerializer

from .permissions import IsAdminUserOrReadOnly


class ExpenseRecordViewSet(viewsets.ModelViewSet):
    queryset = ExpenseRecord.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return FullExpenseRecordSerializer
        else:
            return ExpenseRecordSerializer
