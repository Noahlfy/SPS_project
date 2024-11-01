from rest_framework import serializers

from .models import Head

class HeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Head
        fields = '__all__'
        read_only_fields = ["time"]