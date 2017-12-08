from rest_framework import serializers

from budget.models import Subject

from .item import FullItemSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SimpleSubjectSerializer(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'kind',
            'is_reserves',
            'estimated_amount',
            'actual_amount',
        )
        read_only_fields = fields

    def get_kind(self, obj):
        return obj.get_kind_display()


class FullSubjectSerializer(SimpleSubjectSerializer):
    items = FullItemSerializer(many=True)

    class Meta:
        model = Subject
        fields = (
            'id',
            'name',
            'kind',
            'is_reserves',
            'estimated_amount',
            'actual_amount',
            'items',
        )
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('items')
        return queryset
