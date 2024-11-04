from rest_framework import viewsets
from .models import RightLegMemory
from .serializers import RightLegMemorySerializer

class RightLegMemoryViewSet(viewsets.ModelViewSet):
    queryset = RightLegMemory.objects.all()
    serializer_class = RightLegMemorySerializer