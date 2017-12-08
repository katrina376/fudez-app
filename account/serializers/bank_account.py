from rest_framework import serializers

from account.models import BankAccount, Department

from .department import SimpleDepartmentSerializer


class Parent(object):
    def __init__(self, func):
        self.func = func

    def set_context(self, serializer_field):
        self.value = serializer_field.queryset.get(
            pk=self.func(serializer_field.context))

    def __call__(self):
        return self.value


class BankAccountSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(allow_blank=True)
    bank_code = serializers.CharField(allow_blank=True)
    branch_name = serializers.CharField(allow_blank=True)
    account_name = serializers.CharField(allow_blank=True)
    account = serializers.CharField(allow_blank=True)
    department = serializers.PrimaryKeyRelatedField(
        default=Parent(lambda context: context['department']),
        queryset=Department.objects.all())

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
