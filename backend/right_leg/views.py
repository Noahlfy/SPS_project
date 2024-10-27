from rest_framework import viewsets

from .models import RightLeg

from .serializers import RightLegSerializer

class RightLegViewSet(viewsets.ModelViewSet):
    queryset = RightLeg.objects.all()
    serializer_class = RightLegSerializer