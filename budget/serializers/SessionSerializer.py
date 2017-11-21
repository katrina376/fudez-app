from rest_framework import serializers
from budget.models import Session
from budget.serializers import BookSerializer

class SessionSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Session
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('books')
        return queryset
