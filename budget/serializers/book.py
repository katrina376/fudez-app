from rest_framework import serializers

from budget.models import Book

from .department import BudgetDepartmentSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'description',
            'is_active',
            'announce_date',
            'estimated_income',
            'estimated_expense',
            'actual_income',
            'actual_expense',
        )
        read_only_fields = fields


class FullBookSerializer(serializers.ModelSerializer):
    departments = BudgetDepartmentSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'name',
            'description',
            'is_active',
            'announce_date',
            'estimated_income',
            'estimated_expense',
            'actual_income',
            'actual_expense',
            'departments',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            'projects',
            'projects__subjects',
            'projects__subjects__items',
            'projects__subjects__items__funds',
        )
        return queryset
