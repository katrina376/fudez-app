from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from account.models import BankAccount, Department
from account.serializers import BasicBankAccountSerializer, BankAccountSerializer

from django.shortcuts import get_object_or_404

from .permissions import IsMember

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BankAccountSerializer
        else:
            return BasicBankAccountSerializer

    def get_nested_queryset(self, department_pk):
        return BankAccount.objects.filter(department__pk=department_pk)

    def list(self, request, department_pk=None):
        queryset = self.get_nested_queryset(department_pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def retrieve(self, request, pk=None, department_pk=None):
        queryset = self.get_nested_queryset(department_pk)
        bank_account = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(bank_account)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def create(self, request, department_pk=None):
        input_data = dict(self.request.data)
        if 'department' not in input_data or input_data['department'] != department_pk:
            input_data['department'] = department_pk

        serializer = BasicBankAccountSerializer(data=input_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

    def update(self, request, pk=None, department_pk=None):
        input_data = dict(self.request.data)
        if 'department' not in input_data or input_data['department'] != department_pk:
            input_data['department'] = department_pk

        queryset = self.get_nested_queryset(department_pk)
        bank_account = get_object_or_404(queryset, pk=pk)

        serializer = BasicBankAccountSerializer(bank_account, data=input_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

    def partial_update(self, request, pk=None, department_pk=None):
        input_data = dict(self.request.data)
        input_data.pop('department', None)

        queryset = self.get_nested_queryset(department_pk)
        bank_account = get_object_or_404(queryset, pk=pk)

        serializer = BasicBankAccountSerializer(bank_account, data=input_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

    def destroy(self, request, pk=None, department_pk=None):
        queryset = self.get_nested_queryset(department_pk)
        bank_account = get_object_or_404(queryset, pk=pk)
        bank_account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
