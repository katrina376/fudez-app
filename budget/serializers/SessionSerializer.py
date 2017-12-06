from rest_framework import serializers

from budget.models import Session
from budget.serializers import FullBookSerializer


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class SimpleSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
        )
        read_only_fields = fields


class FullSessionSerializer(serializers.ModelSerializer):
    books = FullBookSerializer(many=True)

    class Meta:
        model = Session
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'books',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('books')
        return queryset
