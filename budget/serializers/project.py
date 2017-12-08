from rest_framework import serializers

from budget.models import Project

from .subject import FullSubjectSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SimpleProjectSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'department',
            'estimated_income',
            'estimated_expense',
            'actual_income',
            'actual_expense',
        )
        read_only_fields = fields

    def get_department(self, obj):
        return obj.department.name


class FullProjectSerializer(SimpleProjectSerializer):
    subjects = FullSubjectSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'department',
            'estimated_income',
            'estimated_expense',
            'actual_income',
            'actual_expense',
            'subjects',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('subjects')
        return queryset
