from rest_framework import serializers
from account.models import Department


class SimpleDepartmentSerializer(serializers.ModelSerializer):
    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return obj.get_kind_display()
    
    class Meta:
        model = Department
        fields = ('id', 'name', 'kind')
