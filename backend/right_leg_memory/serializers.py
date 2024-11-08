from rest_framework import serializers
from .models import RightLegMemory

class RightLegMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RightLegMemory
        fields = '__all__'
        read_only_fields = ['time', 'session']