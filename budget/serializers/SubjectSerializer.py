from rest_framework import serializers
from budget.models import Subject
from budget.serializers import ItemSerializer

class SubjectSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return obj.get_kind_display()

    class Meta:
        model = Subject
        fields = ('id', 'name', 'kind', 'is_reserves', 'estimated_amount', 'actual_amount', 'items')
        read_only_fields = ('id', 'estimated_amount', 'actual_amount', 'items')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('items')
        return queryset
