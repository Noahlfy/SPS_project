from rest_framework import serializers

from .models import Temperature

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"
        read_only_fields = ["time"]