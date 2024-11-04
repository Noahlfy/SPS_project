from rest_framework import viewsets
from .models import ChestMemory
from .serializers import ChestMemorySerializer

class ChestMemoryViewSet(viewsets.ModelViewSet):
    queryset = ChestMemory.objects.all()
    serializer_class = ChestMemorySerializer