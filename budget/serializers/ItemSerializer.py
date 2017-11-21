from rest_framework import serializers
from budget.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'memo', 'addition', 'estimated_amount', 'actual_amount', 'efficiency')
        read_only_fields = ('id', 'actual_amount', 'efficiency')
