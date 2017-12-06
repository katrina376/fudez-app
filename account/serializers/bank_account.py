from rest_framework import serializers

from account.models import BankAccount, Department

from .department import SimpleDepartmentSerializer


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class SimpleBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            'id',
            'bank_name',
            'bank_code',
            'branch_name',
            'account',
            'account_name',
        )
        read_only_fields = fields


class FullBankAccountSerializer(serializers.ModelSerializer):
    department = SimpleDepartmentSerializer

    class Meta:
        model = BankAccount
        fields = (
            'id',
            'bank_name',
            'bank_code',
            'branch_name',
            'account',
            'account_name',
            'department',
        )
        read_only_fields = fields
