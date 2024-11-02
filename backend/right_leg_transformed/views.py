from rest_framework import viewsets

from right_leg_transformed.models import RightLegTransformed

from right_leg_transformed.serializers import RightLegTransformedSerializer

class RightLegTransformedViewSet(viewsets.ModelViewSet):
    queryset = RightLegTransformed.objects.all()
    serializer_class = RightLegTransformedSerializer
