from rest_framework import serializers

from .models import ChestMemory

class ChestMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChestMemory
        fields = '__all__'
