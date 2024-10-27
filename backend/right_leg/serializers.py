from rest_framework import serializers

from .models import RightLeg

class RightLegSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightLeg
        fields = "__all__"
        read_only_fields = "time"
