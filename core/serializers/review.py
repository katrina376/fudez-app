from django.contrib.auth import get_user_model
from rest_framework import serializers


class Parent(object):
    def __init__(self, func):
        self.func = func

    def set_context(self, serializer_field):
        self.value = serializer_field.queryset.get(
            pk=self.func(serializer_field.context))

    def __call__(self):
        return self.value


class ReviewSerializer(serializers.Serializer):
    reviewer_kinds = [get_user_model().PRESIDENT, get_user_model().STAFF, get_user_model().CHIEF]
    reviewer = serializers.PrimaryKeyRelatedField(
        default=Parent(lambda context: context['user']),
        queryset=get_user_model().objects.filter(kind__in=reviewer_kinds))


class ApproveSerializer(ReviewSerializer):
    amount = serializers.IntegerField(default=0)


class RejectSerializer(ReviewSerializer):
    reason = serializers.CharField()
