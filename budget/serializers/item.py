from rest_framework import serializers

from budget.models import Item
from core.serializers import FullFundSerializer


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class SimpleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'memo',
            'addition',
            'estimated_amount',
            'actual_amount',
            'efficiency',
        )
        read_only_fields = fields


class FullItemSerializer(serializers.ModelSerializer):
    funds = FullFundSerializer(many=True)

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'memo',
            'addition',
            'estimated_amount',
            'actual_amount',
            'efficiency',
            'funds',
        )
        read_only_fields = fields
