from rest_framework import serializers
from account.models import Department
from account.serializers import SimpleUserSerializer


class BasicDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id', )

class DepartmentSerializer(serializers.ModelSerializer):
    assistant = SimpleUserSerializer()

    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return obj.get_kind_display()

    class Meta(BasicDepartmentSerializer.Meta):
        read_only_fields = ('id', 'assistant')
