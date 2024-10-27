from rest_framework import serializers

from .models import Chest

class ChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chest
        fields = '__all__'
        read_only_fields = ['time', 'session']