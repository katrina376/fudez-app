from rest_framework import serializers
from account.models import BankAccount
from account.serializers import SimpleDepartmentSerializer


class BasicBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ('id', )

class BankAccountSerializer(BasicBankAccountSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'bank_name', 'bank_code', 'branch_name', 'account', 'account_name')
        read_only_fields = ('id', )
