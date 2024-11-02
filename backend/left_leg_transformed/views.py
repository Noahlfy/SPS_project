from rest_framework import viewsets

from left_leg_transformed.models import LeftLegTransformed

from left_leg_transformed.serializers import LeftLegTransformedSerializer

class LeftLegTransformedViewSet(viewsets.ModelViewSet):
    queryset = LeftLegTransformed.objects.all()
    serializer_class = LeftLegTransformedSerializer