from rest_framework import serializers

from budget.models import Book

from budget.serializers import FullProjectSerializer


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
    projects = FullProjectSerializer(many=True)

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
            'projects',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('projects')
        return queryset
