from rest_framework import serializers
from account.models import Department, User


class SimpleUserSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        return obj.department.name

    class Meta:
        model = User
        fields = ('username', 'name', 'department')

        read_only_fields = fields
