from rest_framework import serializers
from .models import HeadMemory

class HeadMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadMemory
        fields = '__all__'
        read_only_fields = ['time', 'session']