from rest_framework import serializers
from budget.models import Project
from budget.serializers import SubjectSerializer

class ProjectSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        return obj.department.name

    class Meta:
        model = Project
        fields = ('id', 'name', 'department', 'estimated_income', 'estimated_expense', 'actual_income', 'actual_expense', 'subjects')
        read_only_fields = ('id', 'estimated_income', 'estimated_expense', 'actual_income', 'actual_expense', 'subjects')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('subjects')
        return queryset
