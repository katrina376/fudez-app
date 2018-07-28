from rest_framework import serializers

from budget.models import Item
from core.models import Fund, Requirement


class Parent(object):
    def __init__(self, func):
        self.func = func

    def set_context(self, serializer_field):
        self.value = serializer_field.queryset.get(
            pk=self.func(serializer_field.context))

    def __call__(self):
        return self.value


class FundSerializer(serializers.ModelSerializer):
    memo = serializers.CharField(allow_blank=True)
    requirement = serializers.PrimaryKeyRelatedField(
        default=Parent(lambda context: context['requirement']),
        queryset=Requirement.objects.all())

    class Meta:
        model = Fund
        fields = '__all__'

    def validate(self, data):
        item_pk = data['item']
        amount = data['amount']
        item = Item.objects.get(pk=item_pk)

        if (amount + item.actual_amount) > item.estimated_amount:
            raise serializers.ValidationError('Over budget limit.')

        return data


class FullFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = (
            'id',
            'amount',
            'memo',
            'requirement',
            'item',
        )
