from rest_framework import serializers

from .models import LeftLeg


class LeftLegSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftLeg
        fields = "__all__"
        read_only_fields = ["time"]
