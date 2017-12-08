from rest_framework import serializers

from account.models import Department

from .project import FullProjectSerializer


class BudgetDepartmentSerializer(serializers.ModelSerializer):
    projects = FullProjectSerializer(many=True)

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'projects',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('projects')
        return queryset
