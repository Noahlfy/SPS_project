from rest_framework import viewsets
from .models import HeadMemory
from .serializers import HeadMemorySerializer

class HeadMemoryViewSet(viewsets.ModelViewSet):
    queryset = HeadMemory.objects.all()
    serializer_class = HeadMemorySerializer