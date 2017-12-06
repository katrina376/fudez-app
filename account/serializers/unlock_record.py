from rest_framework import serializers

from account.models import UnlockRecord

from .department import SimpleDepartmentSerializer


class UnlockRecordSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(allow_blank=True)

    class Meta:
        model = UnlockRecord
        fields = '__all__'


class SimpleUnlockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlockRecord
        fields = (
            'id',
            'start_time',
            'end_time',
            'reason',
        )
        read_only_fields = fields


class FullUnlockRecordSerializer(serializers.ModelSerializer):
    department = SimpleDepartmentSerializer()

    class Meta:
        model = UnlockRecord
        fields = (
            'id',
            'department',
            'start_time',
            'end_time',
            'reason',
        )
        read_only_fields = fields
