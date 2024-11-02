from rest_framework import serializers

from head_transformed.models import HeadTransformed


class HeadTransformedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadTransformed
        fields = '__all__'
