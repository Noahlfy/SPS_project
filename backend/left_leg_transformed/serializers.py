from rest_framework import serializers

from left_leg_transformed.models import LeftLegTransformed

class LeftLegTransformedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeftLegTransformed
        fields = '__all__'