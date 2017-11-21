from rest_framework import serializers
from account.models import UnlockRecord
#from account.serializers import SimpleDepartmentSerializer


class BasicUnlockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlockRecord
        fields = '__all__'
        read_only_fields = ('id', )

class UnlockRecordSerializer(serializers.ModelSerializer):
    #department = SimpleDepartmentSerializer()

    class Meta:
        model = UnlockRecord
        fields = '__all__'
        read_only_fields = ('id', )
