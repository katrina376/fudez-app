from rest_framework import serializers

from account.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SimpleDepartmentSerializer(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = (
            'id',
            'kind',
            'name',
        )
        read_only_fields = fields

    def get_kind(self, obj):
        return obj.get_kind_display()


class FullDepartmentSerializer(SimpleDepartmentSerializer):
    from .user import SimpleUserSerializer

    assistant = SimpleUserSerializer()

    class Meta:
        model = Department
        fields = (
            'id',
            'kind',
            'name',
            'assistant',
        )
        read_only_fields = fields
