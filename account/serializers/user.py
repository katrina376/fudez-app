from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'name',
            'email',
            'kind',
            'department',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class SimpleUserSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'department',
            'kind',
            'email',
        )
        read_only_fields = fields

    def get_kind(self, obj):
        return obj.get_kind_display()

    def get_department(self, obj):
        return obj.department.name


class FullUserSerializer(serializers.ModelSerializer):
    from .department import SimpleDepartmentSerializer

    department = SimpleDepartmentSerializer()
    assist_departments = SimpleDepartmentSerializer(many=True)

    kind = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'name',
            'department',
            'assist_departments',
            'kind',
            'last_login',
            'create_time',
            'edit_time',
            'is_active',
        )
        read_only_fields = fields

    def get_kind(self, obj):
        return obj.get_kind_display()
