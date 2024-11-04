from rest_framework import viewsets
from .models import LeftLegMemory
from .serializers import LeftLegMemorySerializer

class LeftLegMemoryViewSet(viewsets.ModelViewSet):
    queryset = LeftLegMemory.objects.all()
    serializer_class = LeftLegMemorySerializer