from rest_framework import serializers
from budget.models import Book
from budget.serializers import ProjectSerializer

class BookSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('projects')
        return queryset
