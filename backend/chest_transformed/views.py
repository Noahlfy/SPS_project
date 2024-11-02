from rest_framework import viewsets

from chest_transformed.models import ChestTransformed

from chest_transformed.serializers import ChestTransformedSerializer

class ChestTransformedViewSet(viewsets.ModelViewSet):
    queryset = ChestTransformed.objects.all()
    serializer_class = ChestTransformedSerializer