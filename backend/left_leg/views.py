from rest_framework import viewsets
from .models import LeftLeg
from .serializers import LeftLegSerializer


class LeftLegViewSet(viewsets.ModelViewSet):
    queryset = LeftLeg.objects.all()
    serializer_class = LeftLegSerializer