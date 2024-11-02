from rest_framework import serializers

from right_leg_transformed.models import RightLegTransformed

class RightLegTransformedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RightLegTransformed
        fields = '__all__'