from rest_framework import serializers
from account.models import User
from account.serializers import DepartmentSerializer


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', )

class UserSerializer(BasicUserSerializer):
    department = DepartmentSerializer()
    assist_departments = DepartmentSerializer(many=True)

    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return obj.get_kind_display()

    class Meta(BasicUserSerializer.Meta):
        extra_kwargs = {
                'id': {'read_only': True},
                'password': {'write_only': True},
                'department': {'read_only': True},
                'assist_departments': {'read_only': True}
            }
