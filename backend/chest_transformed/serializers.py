from rest_framework import serializers

from chest_transformed.models import ChestTransformed

class ChestTransformedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChestTransformed
        fields = '__all__'
