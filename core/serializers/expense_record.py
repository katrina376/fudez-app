from rest_framework import serializers

from core.models import ExpenseRecord


class ExpenseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseRecord
        fields = '__all__'


class FullExpenseRecordSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseRecord
        fields = (
            'id',
            'department',
            'kind',
            'memo',
            'date',
            'amount',
            'requirement'
        )
        read_only_fields = fields

    def get_department(self, obj):
        return obj.department.name

    def get_kind(self, obj):
        return obj.get_kind_display()
