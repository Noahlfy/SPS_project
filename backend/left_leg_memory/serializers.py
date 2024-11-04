from rest_framework import serializers
from .models import LeftLegMemory

class LeftLegMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftLegMemory
        fields = '__all__'
